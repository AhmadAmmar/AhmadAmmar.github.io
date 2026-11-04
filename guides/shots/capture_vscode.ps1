# Pictures of VS Code for the beginner guides. Uses a clean temporary profile, and PrintWindow,
# which draws only the VS Code window, so nothing else on the screen can be captured.
param([string]$Out)
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class W { [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out R r);
[DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h,int x,int y,int w,int ht,bool p);
[DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
[DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
[DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
public struct R {public int L,T,Ri,B;} }
"@
$tmp = Join-Path $env:TEMP "vscode_clean_shots2"
$work = Join-Path $tmp "my-site"
New-Item -ItemType Directory -Force $work, "$tmp\profile\User" | Out-Null
Set-Content -Path "$work\index.html" -Value "<h1>Your Name</h1>`n<p>Hello. This is my first web page.</p>" -Encoding utf8
Set-Content -Path "$tmp\profile\User\settings.json" -Value '{"chat.disableAIFeatures":true,"workbench.startupEditor":"none","security.workspace.trust.enabled":false}' -Encoding ascii
git -C $work init -q -b main 2>$null
function Win { (Get-Process Code -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -match "my-site" } | Select-Object -First 1).MainWindowHandle }
function Shot($name) {
  $h = Win
  $r = New-Object W+R; [W]::GetWindowRect($h, [ref]$r) | Out-Null
  $b = New-Object Drawing.Bitmap ($r.Ri-$r.L), ($r.B-$r.T)
  $g = [Drawing.Graphics]::FromImage($b)
  $dc = $g.GetHdc(); [W]::PrintWindow($h, $dc, 2) | Out-Null; $g.ReleaseHdc($dc)
  $b.Save((Join-Path $Out "$name.png")); $g.Dispose(); $b.Dispose()
}
# Keys go only to VS Code: they are skipped if it does not hold the focus.
function Keys($k) {
  $h = Win; [W]::SetForegroundWindow($h) | Out-Null; Start-Sleep -Milliseconds 800
  if ([W]::GetForegroundWindow() -eq $h) { (New-Object -ComObject WScript.Shell).SendKeys($k) } else { Write-Output "skipped $k" }
}
$code = "$env:LOCALAPPDATA\Programs\Microsoft VS Code\bin\code.cmd"
& $code --user-data-dir "$tmp\profile" --extensions-dir "$tmp\ext" --new-window $work "$work\index.html" | Out-Null
Start-Sleep 10
[W]::MoveWindow((Win), 40, 40, 1200, 800, $true) | Out-Null
Start-Sleep 3
Shot "vscode_file_open"
Keys "^+g"; Start-Sleep 3
Shot "vscode_source_control"
Keys "^+e"; Start-Sleep 1
Keys "^``"; Start-Sleep 6
Shot "vscode_terminal"
(Get-Process Code | Where-Object { $_.MainWindowTitle -match "my-site" }) | ForEach-Object { $_.CloseMainWindow() | Out-Null }
