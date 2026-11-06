"""Tests del SCRIPT de auditoría (no del modelo). Deben pasar siempre."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import calculate_audit as audit  # noqa: E402

BIASED = ROOT / "tests" / "fixtures" / "biased_predictions.csv"
FAIR = ROOT / "tests" / "fixtures" / "fair_predictions.csv"


def test_selection_rates_biased():
    df = audit.load_data(BIASED)
    assert audit.selection_rate(df, 0) == pytest.approx(0.75)
    assert audit.selection_rate(df, 1) == pytest.approx(0.25)


def test_disparate_impact_biased():
    assert audit.disparate_impact_ratio(0.25, 0.75) == pytest.approx(1 / 3)


def test_spd_and_eod_biased():
    df = audit.load_data(BIASED)
    tpr_maj = audit.group_confusion(df, 0)["TPR"]
    tpr_min = audit.group_confusion(df, 1)["TPR"]
    assert tpr_maj == pytest.approx(6 / 7)
    assert tpr_min == pytest.approx(3 / 8)
    assert audit.equal_opportunity_difference(tpr_min, tpr_maj) == pytest.approx(
        -0.4821, abs=1e-3
    )
    assert audit.statistical_parity_difference(0.25, 0.75) == pytest.approx(-0.5)


def test_zero_majority_rate_raises():
    with pytest.raises(ZeroDivisionError):
        audit.disparate_impact_ratio(0.5, 0.0)


def test_exit_code_is_1_for_biased_model():
    """El script debe BLOQUEAR un modelo sesgado."""
    assert audit.main(["--data", str(BIASED)]) == 1


def test_exit_code_is_0_for_fair_model():
    """El script debe APROBAR un modelo que cumple la regla 4/5."""
    assert audit.main(["--data", str(FAIR)]) == 0
