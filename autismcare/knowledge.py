"""加载 knowledge/ 下的循证方法库、引用库、安全规则。

数据与代码分离:YAML 存"是什么/规则",这里只负责读取和定位。
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml

# 仓库根目录 = 本文件的上上级(autismcare/ 的父目录)
REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = REPO_ROOT / "knowledge"


def _load_yaml(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"找不到知识库文件:{path}")
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@lru_cache(maxsize=None)
def load_method(method_id: str = "social_stories") -> dict:
    """加载一个循证方法的规则条目。"""
    return _load_yaml(KNOWLEDGE_DIR / "methods" / f"{method_id}.yaml")


@lru_cache(maxsize=None)
def load_citations() -> dict:
    return _load_yaml(KNOWLEDGE_DIR / "citations.yaml")


@lru_cache(maxsize=None)
def load_safety_rules() -> dict:
    return _load_yaml(KNOWLEDGE_DIR / "safety_rules.yaml")


@lru_cache(maxsize=None)
def load_registry() -> dict:
    """加载 EBP 方法总表(methods/_registry.yaml):方法广度骨架。"""
    return _load_yaml(KNOWLEDGE_DIR / "methods" / "_registry.yaml")


@lru_cache(maxsize=None)
def load_skill_domain(domain_id: str) -> dict:
    """加载一个技能领域库(skills/<domain_id>.yaml),如 social_interaction。"""
    return _load_yaml(KNOWLEDGE_DIR / "skills" / f"{domain_id}.yaml")


def list_skill_domains() -> list[str]:
    """列出已有的技能领域库 id(skills/*.yaml)。"""
    skills_dir = KNOWLEDGE_DIR / "skills"
    if not skills_dir.exists():
        return []
    return sorted(p.stem for p in skills_dir.glob("*.yaml"))


@lru_cache(maxsize=None)
def load_standards_cn() -> dict:
    """加载中国指南/标准层(standards_cn.yaml)。"""
    return _load_yaml(KNOWLEDGE_DIR / "standards_cn.yaml")


def methods_for_skill(domain_id: str) -> dict:
    """汇总某技能领域下每个目标建议的方法 id 集合(便于生成器挑选方法)。

    返回 {skill_area_id: [method_id, ...]}(按出现顺序去重)。
    """
    domain = load_skill_domain(domain_id)
    result: dict[str, list[str]] = {}
    for area in domain.get("skill_areas", []) or []:
        seen: list[str] = []
        for tgt in area.get("targets", []) or []:
            for m in tgt.get("methods", []) or []:
                if m not in seen:
                    seen.append(m)
        result[area.get("id", "")] = seen
    return result


def get_skill_area(domain_id: str, area_id: str) -> dict | None:
    """取某领域下某技能区的完整条目;不存在返回 None。"""
    for a in load_skill_domain(domain_id).get("skill_areas", []) or []:
        if a.get("id") == area_id:
            return a
    return None


def find_skill_area(area_id: str) -> tuple[str | None, dict | None]:
    """在所有技能领域里按 area_id 查找,返回 (domain_id, area);找不到返回 (None, None)。"""
    for d in list_skill_domains():
        a = get_skill_area(d, area_id)
        if a is not None:
            return d, a
    return None, None


def generator_ready_methods() -> dict:
    """返回方法总表里 generator_ready 的方法 {id: 条目}。"""
    reg = load_registry()
    return {m["id"]: m for m in reg.get("methods", []) if m.get("generator_ready")}


def recommended_methods_for_area(area: dict) -> list[str]:
    """按出现顺序去重,汇总某技能区各目标建议的方法 id。"""
    seen: list[str] = []
    for tgt in area.get("targets", []) or []:
        for m in tgt.get("methods", []) or []:
            if m not in seen:
                seen.append(m)
    return seen


def pick_method_for_area(area: dict, default: str = "video_modeling") -> str:
    """为某技能区自动挑一个可生成方法:优先方法专属者(非通用视频示范),否则退回默认。

    只在「训练模块」内容类型的可生成方法里挑(排除内容类型不符者,如社交故事)。
    """
    ready = {mid: meta for mid, meta in generator_ready_methods().items()
             if meta.get("content_type") == "training_module"}
    recs = [m for m in recommended_methods_for_area(area) if m in ready]
    for m in recs:
        if m != "video_modeling":
            return m
    return recs[0] if recs else default


def citation_text(cid: str) -> str:
    """把一个引用 id 渲染成可读的一行引用。"""
    cites = load_citations()
    c = cites.get(cid)
    if not c:
        return f"[未知引用:{cid}]"
    authors = c.get("authors", "")
    year = c.get("year", "")
    title = c.get("title", "")
    source = c.get("source", "")
    line = f"{authors} ({year}). {title}. {source}."
    if c.get("verify"):
        line += "  ⚠️需核对原文"
    return line
