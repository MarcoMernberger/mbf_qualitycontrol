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

    def test_filter(self, new_pipegraph):
        q = QCCallback(lambda: ppg.ParameterInvariant("shu", "shu"))
        register_qc("q", q)
        assert get_qc("q") == q
        with pytest.raises(KeyError):
            register_qc("q", q)
        assert len(ppg.util.global_pipegraph.jobs) == 0
        do_qc(lambda name: False)
        assert len(ppg.util.global_pipegraph.jobs) == 0
        do_qc(lambda name: "q" in name)
        assert len(ppg.util.global_pipegraph.jobs) == 1

    def test_assert_images_equal_inside_class(self):
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


def test_assert_images_equal():
    assert_image_equal(
        Path(__file__).parent
        / "base_images"
        / "test_qc"
        / "_"
        / "test_assert_images_equal.png"
    )
    with pytest.raises(ValueError) as e:  # here the baseline image does not exist
        assert_image_equal(
            Path(__file__).parent
            / "base_images"
            / "test_qc"
            / "_"
            / "test_assert_images_equal.png",
            "_b",
        )
    # should_path overwrites suffix
    assert_image_equal(
            Path(__file__).parent
            / "base_images"
            / "test_qc"
            / "_"
            / "test_assert_images_equal.png",
            "_b",
        should_path = Path(__file__).parent
            / "base_images"
            / "test_qc"
            / "_"
            / "test_assert_images_equal.png",
        )

    assert "Base_line image not found" in str(e.value)
    with pytest.raises(ValueError) as e:  # here it is different
        assert_image_equal(
            Path(__file__).parent
            / "base_images"
            / "test_qc"
            / "_"
            / "test_assert_images_equal.png",
            suffix="_c",
        )
    assert "Image files did not match" in str(e.value)

    with pytest.raises(IOError) as e:
        assert_image_equal("does not exist")
    assert "not created" in str(e.value)

    # with pytest.raises(ValueError) as e: #here it is different
    with pytest.raises(ValueError) as e:  # here it is different
        assert_image_equal(
        Path(__file__).parent
        / "base_images"
        / "test_qc"
        / "_"
        / "test_assert_images_equal.png",
        suffix="_d",
    )
    assert 'do not match expected size' in str(e.value)
