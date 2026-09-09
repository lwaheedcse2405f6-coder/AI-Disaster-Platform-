pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
  }

  stages {
    stage('Source change report') {
      steps {
        powershell '''
$ErrorActionPreference = "Stop"
$projectRoot = $env:WORKSPACE
$reportPath = Join-Path $projectRoot "jenkins-source-report.txt"
$lines = [System.Collections.Generic.List[string]]::new()

function Write-ReportLine {
  param([string]$Line)
  $lines.Add($Line)
  Write-Host $Line
}

Write-ReportLine "================ SOURCE CHANGE REPORT ================"
$git = Get-Command git -ErrorAction SilentlyContinue
$gitDirectory = Join-Path $projectRoot ".git"

if (-not $git -or -not (Test-Path $gitDirectory)) {
  Write-ReportLine "Git repository            : not detected"
  Write-ReportLine "Jenkins Changes tab       : requires Pipeline script from SCM and Git commits"
  Write-ReportLine "See JENKINS_SETUP.md before the next build."
} else {
  $branch = (& $git.Source -C $projectRoot branch --show-current).Trim()
  $revision = (& $git.Source -C $projectRoot rev-parse --short HEAD).Trim()
  $commit = (& $git.Source -C $projectRoot log -1 --format=%s).Trim()
  $author = (& $git.Source -C $projectRoot log -1 --format=%an).Trim()
  $changedFiles = @(& $git.Source -C $projectRoot diff --name-status HEAD~1 HEAD 2>$null)

  Write-ReportLine "Git branch                : $branch"
  Write-ReportLine "Current commit            : $revision"
  Write-ReportLine "Commit message            : $commit"
  Write-ReportLine "Commit author             : $author"
  Write-ReportLine ""
  Write-ReportLine "Files changed since previous commit:"
  if ($changedFiles.Count -eq 0) {
    Write-ReportLine "- No file changes found. This can be the first commit."
  } else {
    foreach ($file in $changedFiles) {
      Write-ReportLine "- $file"
    }
  }
}

Write-ReportLine "========================================================"
$lines | Set-Content -Path $reportPath -Encoding utf8
'''
      }
    }

    stage('Backend: install dependencies') {
      steps {
        dir('backend') {
          bat '''
where python >nul 2>nul
if errorlevel 1 (
  if exist ..\\venv\\Scripts\\python.exe (
    ..\\venv\\Scripts\\python.exe --version >nul 2>nul
    if not errorlevel 1 set "PYTHON_EXE=..\\venv\\Scripts\\python.exe"
  )
  if not defined PYTHON_EXE (
    echo Python was not found on PATH and no working project virtual environment was found.
    echo Install Python 3, enable "Add python.exe to PATH", then restart Jenkins.
    exit /b 1
  )
) else (
  set "PYTHON_EXE=python"
)
if exist .jenkins-venv rmdir /s /q .jenkins-venv
"%PYTHON_EXE%" -m venv .jenkins-venv
call .jenkins-venv\\Scripts\\activate.bat
python -m pip install --upgrade pip
pip install -r ..\\requirements.txt
'''
        }
      }
    }

    stage('Frontend: install and build') {
      steps {
        dir('frontend') {
          bat '''
npm.cmd ci
npm.cmd run build
'''
        }
      }
    }

    stage('Run smoke test and print dashboard') {
      steps {
        powershell '''
$ErrorActionPreference = "Stop"

$projectRoot = $env:WORKSPACE
$backendDir = Join-Path $projectRoot "backend"
$pythonExe = Join-Path $backendDir ".jenkins-venv\\Scripts\\python.exe"
$backendOutLog = Join-Path $projectRoot "backend-jenkins-out.log"
$backendErrLog = Join-Path $projectRoot "backend-jenkins-err.log"
$dashboardReport = Join-Path $projectRoot "jenkins-build-dashboard.txt"
$ciPort = 18000
$healthUrl = "http://127.0.0.1:$ciPort/health"
$dashboardUrl = "http://127.0.0.1:$ciPort/api/dashboard"
$lines = [System.Collections.Generic.List[string]]::new()

function Write-DashboardLine {
  param([string]$Line = "")
  $lines.Add($Line)
  Write-Host $Line
}

Write-Host "Starting FastAPI backend for Jenkins smoke test on port $ciPort..."
$backend = Start-Process `
  -FilePath $pythonExe `
  -ArgumentList @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "$ciPort") `
  -WorkingDirectory $backendDir `
  -PassThru `
  -WindowStyle Hidden `
  -RedirectStandardOutput $backendOutLog `
  -RedirectStandardError $backendErrLog

try {
  Write-Host "Waiting for backend health endpoint..."
  $ready = $false
  for ($i = 1; $i -le 30; $i++) {
    try {
      $health = Invoke-RestMethod -Uri $healthUrl -TimeoutSec 2
      if ($health.status -eq "ok") {
        $ready = $true
        break
      }
    } catch {
      Start-Sleep -Seconds 1
    }
  }

  if (-not $ready) {
    throw "Backend did not become healthy at $healthUrl. Review backend-jenkins-err.log."
  }

  $dashboard = Invoke-RestMethod -Uri $dashboardUrl -TimeoutSec 5

  Write-DashboardLine ""
  Write-DashboardLine "================ AI DISASTER PLATFORM DASHBOARD ================"
  Write-DashboardLine "Backend health            : OK"
  Write-DashboardLine "Frontend production build : OK"
  Write-DashboardLine "Smoke-test API            : $dashboardUrl"
  Write-DashboardLine "Total assessments         : $($dashboard.total_assessments)"
  Write-DashboardLine "High risk regions         : $($dashboard.high_risk_regions)"
  Write-DashboardLine "Active incidents          : $($dashboard.active_incidents)"
  Write-DashboardLine "Average risk score        : $($dashboard.average_risk_score)"
  Write-DashboardLine ""
  Write-DashboardLine "Latest assessments:"
  foreach ($item in $dashboard.latest_assessments) {
    Write-DashboardLine ("- {0} | {1} | risk {2} | impact {3}" -f $item.region, $item.risk_level, $item.overall_risk_score, $item.impact_score)
  }
  Write-DashboardLine ""
  Write-DashboardLine "Incidents:"
  foreach ($item in $dashboard.incidents) {
    Write-DashboardLine ("- {0} | {1} | {2} | severity {3}" -f $item.title, $item.region, $item.status, $item.severity)
  }
  Write-DashboardLine "================================================================="
  Write-DashboardLine ""
} finally {
  $lines | Set-Content -Path $dashboardReport -Encoding utf8
  if ($backend -and -not $backend.HasExited) {
    Write-Host "Stopping backend smoke-test process..."
    Stop-Process -Id $backend.Id -Force
  }
}
'''
      }
    }
  }

  post {
    always {
      archiveArtifacts artifacts: 'backend-jenkins-*.log, jenkins-*-report.txt, frontend/dist/**', allowEmptyArchive: true
    }
  }
}
