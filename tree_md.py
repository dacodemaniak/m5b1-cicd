import os
import argparse
from pathlib import Path

def should_ignore(path, ignore_dirs=None, ignore_files=None):
    """Détermine si un chemin doit être ignoré"""
    if ignore_dirs is None:
        ignore_dirs = ['.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv', 'env']
    if ignore_files is None:
        ignore_files = ['.DS_Store', '.gitignore', '.gitattributes']
    
    path_name = path.name
    if path.is_dir() and path_name in ignore_dirs:
        return True
    if path.is_file() and path_name in ignore_files:
        return True
    return False

def get_file_size(file_path):
    """Retourne la taille d'un fichier en format lisible"""
    try:
        size = file_path.stat().st_size
        if size == 0:
            return "(vide)"
        elif size < 1024:
            return f"({size} B)"
        elif size < 1024 * 1024:
            return f"({size // 1024} KB)"
        else:
            return f"({size // (1024 * 1024)} MB)"
    except:
        return "(erreur)"

def create_markdown_tree(directory, output_file=None, max_depth=None, show_size=False, include_hidden=False):
    """
    Crée une arborescence au format Markdown
    
    Args:
        directory: Répertoire racine
        output_file: Fichier de sortie (None pour afficher à l'écran)
        max_depth: Profondeur maximale (None pour illimité)
        show_size: Afficher la taille des fichiers
        include_hidden: Inclure les fichiers/dossiers cachés
    """
    root_path = Path(directory).resolve()
    
    if not root_path.exists():
        print(f"Erreur: Le répertoire {directory} n'existe pas")
        return
    
    markdown_lines = []
    markdown_lines.append(f"# Arborescence de `{root_path}`\n")
    markdown_lines.append("```")
    
    def add_to_tree(current_path, prefix="", depth=0):
        if max_depth and depth > max_depth:
            return
        
        # Ignorer certains fichiers/dossiers
        if not include_hidden and current_path.name.startswith('.'):
            return
        if should_ignore(current_path):
            return
        
        if current_path == root_path:
            markdown_lines.append(f"{current_path.name}/")
        else:
            markdown_lines.append(f"{prefix}{current_path.name}/" if current_path.is_dir() else 
                                 f"{prefix}{current_path.name} {get_file_size(current_path) if show_size and current_path.is_file() else ''}")
        
        if current_path.is_dir():
            try:
                children = sorted([p for p in current_path.iterdir() 
                                 if include_hidden or not p.name.startswith('.')])
                
                for index, child in enumerate(children):
                    if should_ignore(child) and not include_hidden:
                        continue
                    
                    is_last = index == len(children) - 1
                    connector = "└── " if is_last else "├── "
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    
                    add_to_tree(child, new_prefix, depth + 1)
                    markdown_lines[-1] = prefix + connector + markdown_lines[-1].split(prefix + connector)[-1] if prefix + connector in markdown_lines[-1] else markdown_lines[-1]
                    
            except PermissionError:
                markdown_lines.append(f"{prefix}    [Permission denied]")
    
    add_to_tree(root_path)
    markdown_lines.append("```\n")
    
    # Statistiques
    file_count = sum(1 for f in root_path.rglob('*') if f.is_file() and not should_ignore(f))
    dir_count = sum(1 for d in root_path.rglob('*') if d.is_dir() and not should_ignore(d))
    
    markdown_lines.append("## Statistiques")
    markdown_lines.append(f"- 📁 Dossiers: {dir_count}")
    markdown_lines.append(f"- 📄 Fichiers: {file_count}")
    markdown_lines.append(f"- 📍 Répertoire: `{root_path}`")
    
    result = "\n".join(markdown_lines)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Arborescence sauvegardée dans: {output_file}")
    else:
        print(result)
    
    return result

def main():
    parser = argparse.ArgumentParser(description="Générateur d'arborescence Markdown")
    parser.add_argument("directory", nargs="?", default=".", help="Répertoire à analyser (défaut: courant)")
    parser.add_argument("-o", "--output", help="Fichier de sortie Markdown")
    parser.add_argument("-d", "--depth", type=int, help="Profondeur maximale")
    parser.add_argument("-s", "--size", action="store_true", help="Afficher les tailles des fichiers")
    parser.add_argument("-a", "--all", action="store_true", help="Inclure les fichiers cachés")
    
    args = parser.parse_args()
    
    create_markdown_tree(
        directory=args.directory,
        output_file=args.output,
        max_depth=args.depth,
        show_size=args.size,
        include_hidden=args.all
    )

if __name__ == "__main__":
    main()