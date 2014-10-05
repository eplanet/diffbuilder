import os, sys
import argparse

from diffbuilder.diffbuilder import DiffBuilder

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Produit la différence entre deux arborescences.')
    parser.add_argument('-r', '--reference', metavar='/tmp/reference', type=str, required=True, help='La racine du répertoire de référence')
    parser.add_argument('-c', '--compare', metavar='/tmp/compare', type=str, required=True, help='La racine du répertoire à comparer')
    parser.add_argument('-o', '--output', metavar='/tmp/output', type=str, required=True, help='Le dossier de destination')
    parser.add_argument('-s', '--script', metavar='/tmp/outputscript.sh', type=argparse.FileType('w', encoding='UTF-8'), required=True, help='Le script de remove à appliquer __avant__ la copie')
    args = vars(parser.parse_args(sys.argv[1:]))
    if not os.path.exists(args["reference"]) or not os.path.exists(args["compare"]) or not os.path.exists(args["output"]) :
        print("Input directories must exist")
        sys.exit(1)
    db = DiffBuilder(args["reference"], args["compare"], args["output"], args["script"])
    db.generateDiff()