"""Execute and save the demo using the current interpreter, without registration."""

import sys
from pathlib import Path

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient


def main():
    if sys.version_info[:3] != (3, 12, 10):
        raise RuntimeError("Run with Python 3.12.10 from the project .venv")
    path = Path(__file__).with_name("preprocessing_demo.ipynb")
    notebook = nbformat.read(path, as_version=4)
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [
        sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"
    ]
    client = NotebookClient(
        notebook,
        km=manager,
        timeout=120,
        allow_errors=False,
        resources={"metadata": {"path": str(path.parent)}},
    )
    try:
        client.execute()
    finally:
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
    nbformat.validate(notebook)
    cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
    assert all(cell.execution_count is not None for cell in cells)
    assert not any(output.output_type == "error"
                   for cell in cells for output in cell.outputs)
    nbformat.write(notebook, path)
    print(f"Executed and saved {len(cells)} code cells; no errors: {path}")


if __name__ == "__main__":
    main()
