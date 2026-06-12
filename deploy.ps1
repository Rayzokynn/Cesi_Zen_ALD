<#
.SYNOPSIS
    Script de déploiement automatique en une seule commande pour CESIZen depuis Windows.
.DESCRIPTION
    Ce script automatise la copie du fichier docker-compose.prod.yml vers la VM distante
    sous le nom de 'docker-compose.yml', puis exécute les commandes Docker nécessaires
    sur la VM via SSH pour déployer la nouvelle version.
.PARAMETER VMHost
    L'adresse IP ou le nom d'hôte de la VM cible.
.PARAMETER VMUser
    L'utilisateur SSH pour se connecter à la VM.
.PARAMETER SSHKeyPath
    Le chemin de la clé privée SSH (facultatif si ssh-agent est utilisé ou si SSH sans mot de passe).
.PARAMETER VMDeployPath
    Le dossier de destination sur la VM (par défaut ~/cesizen).
.PARAMETER RepoNamespace
    Le nom d'espace/organisation du dépôt sur GHCR (par défaut rayzokynn/cesi_zen_ald).
.PARAMETER GitHubUser
    Votre nom d'utilisateur GitHub (facultatif, pour se reconnecter à GHCR).
.PARAMETER GitHubPAT
    Votre Personal Access Token GitHub (facultatif, pour se reconnecter à GHCR).
.EXAMPLE
    .\deploy.ps1 -VMHost "192.168.56.101" -VMUser "ubuntu" -SSHKeyPath "~\.ssh\id_rsa"
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $true)]
    [string]$VMHost,

    [Parameter(Mandatory = $true)]
    [string]$VMUser,

    [Parameter(Mandatory = $false)]
    [string]$SSHKeyPath,

    [Parameter(Mandatory = $false)]
    [string]$VMDeployPath = "~/cesizen",

    [Parameter(Mandatory = $false)]
    [string]$RepoNamespace = "rayzokynn/cesi_zen_ald",

    [Parameter(Mandatory = $false)]
    [string]$GitHubUser,

    [Parameter(Mandatory = $false)]
    [string]$GitHubPAT
)

$ErrorActionPreference = "Stop"

Write-Host "🚀 Début du déploiement automatique de CESIZen..." -ForegroundColor Cyan

# 1. Vérification des fichiers locaux
$LocalComposePath = Join-Path $PSScriptRoot "docker-compose.prod.yml"
if (-not (Test-Path $LocalComposePath)) {
    Write-Error "Fichier docker-compose.prod.yml introuvable à l'emplacement $LocalComposePath."
}

# Préparation des arguments SSH / SCP
$SSHKeyArg = ""
$SCPKeyArg = ""
if ($SSHKeyPath) {
    # Conversion éventuelle de ~ vers le dossier utilisateur
    if ($SSHKeyPath.StartsWith("~")) {
        $SSHKeyPath = $SSHKeyPath.Replace("~", $env:USERPROFILE)
    }
    if (-not (Test-Path $SSHKeyPath)) {
        Write-Error "La clé SSH spécifiée est introuvable : $SSHKeyPath"
    }
    $SSHKeyArg = "-i `"$SSHKeyPath`""
    $SCPKeyArg = "-i `"$SSHKeyPath`""
}

# 2. Création du répertoire distant via SSH
Write-Host "📂 Création du dossier distant $VMDeployPath sur la VM..." -ForegroundColor Yellow
$CreateFolderCmd = "ssh $SSHKeyArg $VMUser@$VMHost 'mkdir -p $VMDeployPath'"
Invoke-Expression $CreateFolderCmd

# 3. Interpolation locale et copie du docker-compose.prod.yml vers docker-compose.yml
Write-Host "📤 Interpolation et copie du compose vers la VM..." -ForegroundColor Yellow
$TempCompose = [System.IO.Path]::GetTempFileName()
$ComposeContent = Get-Content $LocalComposePath -Raw
$ComposeContent = $ComposeContent -replace '\$\{REPO_LOWER\}', $RepoNamespace
Set-Content -Path $TempCompose -Value $ComposeContent

$SCPCmd = "scp $SCPKeyArg `"$TempCompose`" $VMUser@$VMHost`:$VMDeployPath/docker-compose.yml"
Invoke-Expression $SCPCmd
Remove-Item $TempCompose

# 4. Connexion et redémarrage des conteneurs via SSH
Write-Host "🐳 Téléchargement des images et démarrage des conteneurs sur la VM..." -ForegroundColor Yellow

$RemoteCommands = @(
    "cd $VMDeployPath"
)

if ($GitHubUser -and $GitHubPAT) {
    Write-Host "🔑 Authentification auprès de GitHub Container Registry..." -ForegroundColor Yellow
    $RemoteCommands += "echo `"$GitHubPAT`" | docker login ghcr.io -u $GitHubUser --password-stdin"
}

$RemoteCommands += "docker compose pull"
$RemoteCommands += "docker compose up -d --remove-orphans"
$RemoteCommands += "docker compose ps"

# Joindre toutes les commandes par des double-esperluettes (&&) pour assurer l'arrêt si l'une échoue
$SSHCommands = $RemoteCommands -join " && "

$SSHRunCmd = "ssh $SSHKeyArg $VMUser@$VMHost `"$SSHCommands`""
Invoke-Expression $SSHRunCmd

Write-Host "✨ Déploiement terminé avec succès !" -ForegroundColor Green
