
from dataclasses import dataclass, field
from typing import Callable, List, Any, Optional

from DSL4Pipelines.src.metamodel.artefacts.artefacts import Artefact
from DSL4Pipelines.src.metamodel.core.structure import Element


@dataclass
class Rule(Element):
    name: str = "noName"  # Un nom lisible pour la règle
    weight: float = 0.0  # Un poids pour indiquer l'importance de la règle (optionnel)
    # La fonction renvoie True peu importent les arguments reçus (*args, **kwargs)
    func: Callable = lambda *args, **kwargs: True
    def __str__(self):
        return f"Rule: {self.name} (weight: {self.weight})"
    def evaluate(self, *args, **kwargs) -> Any:
        """Exécute la fonction de la règle avec les arguments donnés."""
        return self.func(*args, **kwargs)

# C'est ici que toutes les règles seront "stockées" automatiquement
RULE_REGISTRY: List[Rule] = []

def eval_rule(name: str, weight: float = 1.0) -> Callable[[Callable], Callable]:
    """Le décorateur qui enregistre les fonctions des experts."""
    def decorator(func: Callable):
        # On crée l'entrée dans le registre
        metadata = Rule(name=name, weight=weight, func=func)
        RULE_REGISTRY.append(metadata)

        # On renvoie la fonction originale sans la modifier
        return func
    return decorator

#La structure de résultat que chaque règle doit retourner

@dataclass
class EvaluationResult:
    label: str
    success: bool
    score: float  # Entre 0.0 et 1.0
    evidence: str # Justification (ex: "J'ai trouvé 12 fichiers FR")
    def __str__(self):
        icon = "✅" if self.success else "❌"
        return f"{icon} {self.label}: {self.evidence} (score: {self.score:.2f})"

@dataclass
class RuleReport(Artefact):
    type: str = "RuleReport"
    rule: Optional[Rule] = (
        None  # e.g., ArtefactCatalog.ACCESS.PUBLIC, ArtefactCatalog.ACCESS.PRIVATE, etc.
    )
    results: List[EvaluationResult] = field(default_factory=list)
    avg_score: float = 0.0
    status: str = "Red"  # Green, Orange, Red

    def __str__(self):
        icon = "🟢" \
            if self.status == "Green" \
            else "🟠" if self.status == "Orange" else "🔴"
        details = "\n    ".join(str(r) for r in self.results)
        return f"{icon} {self.rule.name:<25} | Score: {self.avg_score:.2f} | \n Details:\n    {details} "