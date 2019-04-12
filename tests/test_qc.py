import pytest
from pathlib import Path
import pypipegraph as ppg
from mbf_qualitycontrol import register_qc, get_qc, do_qc, QCCallback
from mbf_qualitycontrol.testing import assert_image_equal


class TestRegistration:
    def test_register_get(self, new_pipegraph):
        q = QCCallback(lambda: ppg.ParameterInvariant("shu", "shu"))
        register_qc("q", q)
        assert get_qc("q") == q
        with pytest.raises(KeyError):
            register_qc("q", q)
        assert len(ppg.util.global_pipegraph.jobs) == 0
        do_qc()
        assert len(ppg.util.global_pipegraph.jobs) == 1
        new_pipegraph.new_pipegraph()
        assert len(ppg.util.global_pipegraph.jobs) == 0
        do_qc()
        assert len(ppg.util.global_pipegraph.jobs) == 0
        with pytest.raises(ValueError):
            register_qc("r", ppg.ParameterInvariant("sha", "sha"))
        with pytest.raises(ValueError):
            r = ppg.ParameterInvariant("shi", "shi")
            QCCallback(r)


def test_assert_images_equal():
    assert_image_equal(
        Path(__file__).parent
        / "base_images"
        / "test_qc"
        / "_"
        / "test_assert_images_equal.png"
    )
    with pytest.raises(ValueError):
        assert_image_equal(
            Path(__file__).parent
            / "base_images"
            / "test_qc"
            / "_"
            / "test_assert_images_equal.png",
            "_b",
        )
