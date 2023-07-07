from dotenv import load_dotenv

from movie_app import create_app


def main():
    load_dotenv()
    app = create_app()
    app.run(debug=True)


if __name__ == '__main__':
    main()
