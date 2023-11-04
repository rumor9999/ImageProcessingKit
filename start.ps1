Write-Host "create venv..."

# Get the directory where the script is located
$scriptDir = $PSScriptRoot

# Set the virtual environment directory and project directory
$venvDir = Join-Path $scriptDir "venv"  # Create the venv directory under the script directory

# Activate the virtual environment
$venvScript = Join-Path $venvDir "Scripts\Activate"

# Check if the virtual environment directory already exists
if (-Not (Test-Path $venvDir -PathType Container)) {
    # Create a virtual environment
    python -m venv $venvDir

    cmd /c $venvScript

    # Install the required dependencies
    pip install -r "requirements.txt"

    # Print a success message
    Write-Host "create venv done."
} else {
    Write-Host "venv exists."
}

cmd /c $venvScript

py .\main.py
