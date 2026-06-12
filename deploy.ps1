<#
.SYNOPSIS
    Script de deploiement automatique en une seule commande pour CESIZen depuis Windows.
.DESCRIPTION
    Ce script automatise la copie du fichier docker-compose.prod.yml vers la VM distante
    sous le nom de 'docker-compose.yml', puis execute les commandes Docker necessaires
    sur la VM via SSH pour deployer la nouvelle version.
.PARAMETER VMHost
    L'adresse IP ou le nom d'hote de la VM cible.
.PARAMETER VMUser
    L'utilisateur SSH pour se connecter a la VM.
.PARAMETER VMPort
    Le port SSH pour se connecter a la VM (par defaut 22, utile si reseau NAT avec redirection de port).
.PARAMETER SSHKeyPath
    Le chemin de la cle privee SSH (facultatif si ssh-agent est utilise ou si SSH sans mot de passe).
.PARAMETER VMDeployPath
    Le dossier de destination sur la VM (par defaut ~/cesizen).
.PARAMETER RepoNamespace
    Le nom d'espace/organisation du depot sur GHCR (par defaut rayzokynn/cesi_zen_ald).
.PARAMETER GitHubUser
    Votre nom d'utilisateur GitHub (facultatif, pour se reconnecter a GHCR).
.PARAMETER GitHubPAT
    Votre Personal Access Token GitHub (facultatif, pour se reconnecter a GHCR).
.EXAMPLE
    .\deploy.ps1 -VMHost "127.0.0.1" -VMPort 2222 -VMUser "vboxuser" -RunMigrations -SeedDB
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $true)]
    [string]$VMHost,

    [Parameter(Mandatory = $true)]
    [string]$VMUser,

    [Parameter(Mandatory = $false)]
    [int]$VMPort = 22,

    [Parameter(Mandatory = $false)]
    [string]$SSHKeyPath,

    [Parameter(Mandatory = $false)]
    [string]$VMDeployPath = "~/cesizen",

    [Parameter(Mandatory = $false)]
    [string]$RepoNamespace = "rayzokynn/cesi_zen_ald",

    [Parameter(Mandatory = $false)]
    [string]$GitHubUser,

    [Parameter(Mandatory = $false)]
    [string]$GitHubPAT,

    [Parameter(Mandatory = $false)]
    [switch]$RunMigrations,

    [Parameter(Mandatory = $false)]
    [switch]$SeedDB
)

$ErrorActionPreference = "Stop"

# Fonction utilitaire pour executer des commandes externes et arreter le script en cas d'erreur
function Invoke-ExternalCommand {
    param (
        [string]$CommandLine
    )
    # Reinitialisation de LASTEXITCODE
    $global:LASTEXITCODE = 0
    Invoke-Expression $CommandLine
    if ($global:LASTEXITCODE -ne 0) {
        Write-Error "La commande externe a echoue avec le code de sortie $global:LASTEXITCODE."
        exit $global:LASTEXITCODE
    }
}

Write-Host "Debut du deploiement automatique de CESIZen..." -ForegroundColor Cyan

# 1. Verification des fichiers locaux
$LocalComposePath = Join-Path $PSScriptRoot "docker-compose.prod.yml"
if (-not (Test-Path $LocalComposePath)) {
    Write-Error "Fichier docker-compose.prod.yml introuvable a l'emplacement $LocalComposePath."
    exit 1
}

# Preparation des arguments SSH / SCP
$SSHKeyArg = ""
$SCPKeyArg = ""
if ($SSHKeyPath) {
    # Conversion eventuelle de ~ vers le dossier utilisateur
    if ($SSHKeyPath.StartsWith("~")) {
        $SSHKeyPath = $SSHKeyPath.Replace("~", $env:USERPROFILE)
    }
    if (-not (Test-Path $SSHKeyPath)) {
        Write-Error "La cle SSH specifiee est introuvable : $SSHKeyPath"
        exit 1
    }
    $SSHKeyArg = "-i `"$SSHKeyPath`""
    $SCPKeyArg = "-i `"$SSHKeyPath`""
}

# 2. Creation du repertoire distant via SSH
Write-Host "Creation du dossier distant $VMDeployPath sur la VM (Port: $VMPort)..." -ForegroundColor Yellow
$CreateFolderCmd = "ssh -p $VMPort $SSHKeyArg $VMUser@$VMHost 'mkdir -p $VMDeployPath'"
Invoke-ExternalCommand -CommandLine $CreateFolderCmd

# 3. Interpolation locale et copie du docker-compose.prod.yml vers docker-compose.yml
Write-Host "Interpolation et copie du compose vers la VM..." -ForegroundColor Yellow
$TempCompose = [System.IO.Path]::GetTempFileName()
$ComposeContent = Get-Content $LocalComposePath -Raw
$ComposeContent = $ComposeContent -replace '\$\{REPO_LOWER\}', $RepoNamespace
Set-Content -Path $TempCompose -Value $ComposeContent

$SCPCmd = "scp -P $VMPort $SCPKeyArg `"$TempCompose`" $VMUser@$VMHost`:$VMDeployPath/docker-compose.yml"
Invoke-ExternalCommand -CommandLine $SCPCmd
Remove-Item $TempCompose

# 4. Connexion et redemarrage des conteneurs via SSH
Write-Host "Telechargement des images et demarrage des conteneurs sur la VM..." -ForegroundColor Yellow

$RemoteCommands = @(
    "cd $VMDeployPath"
)

if ($GitHubUser -and $GitHubPAT) {
    Write-Host "Authentification aupres de GitHub Container Registry..." -ForegroundColor Yellow
    $RemoteCommands += "echo `"$GitHubPAT`" | docker login ghcr.io -u $GitHubUser --password-stdin"
}

$RemoteCommands += "docker compose pull"
$RemoteCommands += "docker compose up -d --remove-orphans"

if ($RunMigrations) {
    Write-Host "Execution des migrations sur la VM..." -ForegroundColor Yellow
    $RemoteCommands += "docker compose exec -T backend python manage.py migrate"
}

if ($SeedDB) {
    Write-Host "Peuplement de la base de donnees sur la VM..." -ForegroundColor Yellow
    $RemoteCommands += "docker compose exec -T backend python manage.py seed_db"
}

$RemoteCommands += "docker compose ps"

# Joindre toutes les commandes par des double-esperluettes (&&) pour assurer l'arret si l'une echoue
$SSHCommands = $RemoteCommands -join " && "

$SSHRunCmd = "ssh -p $VMPort $SSHKeyArg $VMUser@$VMHost `"$SSHCommands`""
Invoke-ExternalCommand -CommandLine $SSHRunCmd

Write-Host "Deploiement termine avec succes !" -ForegroundColor Green
