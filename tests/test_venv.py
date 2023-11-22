import auto_repo


def test_create_venv_default_name(tmpdir):
    auto_repo.create_venv(tmpdir.dirpath())

    assert tmpdir.ensure_dir(".venv")


def test_create_venv_with_custom_name(tmpdir):
    auto_repo.create_venv(tmpdir.dirpath(), "pytest")

    assert tmpdir.ensure_dir("pytest")
