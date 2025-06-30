import blendertoolbox.cli as cli
import blendertoolbox as bt
from pathlib import Path

def test_cli_invokes_render(monkeypatch, tmp_path):
    called = {}
    def fake_render(args):
        called['args'] = args
    monkeypatch.setattr(bt, 'render_mesh_default', fake_render)
    mesh = Path(__file__).resolve().parent.parent / 'demos' / 'test.obj'
    output = tmp_path / 'out.png'
    cli.main([str(mesh), '-o', str(output)])
    assert called['args']['mesh_path'] == str(mesh)
    assert called['args']['output_path'] == str(output)
