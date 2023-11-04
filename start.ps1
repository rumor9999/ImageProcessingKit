Write-Host "create venv..."

# 获取脚本所在的目录
$scriptDir = $PSScriptRoot

# 设置虚拟环境目录和项目目录
$venvDir = Join-Path $scriptDir "venv"  # 在脚本目录下创建venv目录

# 检查是否已经存在虚拟环境目录
if (-Not (Test-Path $venvDir -PathType Container)) {
    # 创建虚拟环境
    python -m venv $venvDir

    # 激活虚拟环境
    $venvScript = Join-Path $venvDir "Scripts\Activate"
    cmd /c $venvScript

    # 安装所需依赖项
    pip install -r "requirements.txt"

    # 打印成功消息
    Write-Host "create venv done."
} else {
    Write-Host "venv exists."
}

py .\main.py