def test_skeleton_import():
    import cursos
    assert hasattr(cursos, "__all__")
