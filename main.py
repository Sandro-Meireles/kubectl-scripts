import questionary

from core.script import Script


def main():
    scripts = Script.get_scripts()
    scripts_names = list(
        map(lambda script: f'{script.__name__} - {script.Meta.description}',
            scripts)
        )

    response = questionary.select(
        'Which script you want to run?',
        scripts_names
        ).ask()

    index = scripts_names.index(response)

    script = scripts[index]
    script()


if __name__ == '__main__':
    main()
