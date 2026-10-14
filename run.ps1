# NoseClicker AI PowerShell Launcher
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

if (Get-Command python -ErrorAction SilentlyContinue) {
    python main.py $args
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    py main.py $args
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    python3 main.py $args
} else {
    python main.py $args
}
