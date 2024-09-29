#author: Vijay Sankar C
#date: 25/07/24
#description: Create a command-line tool using Click that takes a list of names as input and filters out any names starting with the letter 'p'.

#import sec
import click

@click.command()
@click.argument('names',nargs=-1)

#funct for filtering
def filter_names(names):
    try:
        filtered_names=[name for name in names if not name.lower().startswith('p')]
        for name in filtered_names:
            click.echo(name)
    except Exception as e:
        print(f"Error Occured: {e}")

#Entry point of script
if __name__=="__main__":
    filter_names()


