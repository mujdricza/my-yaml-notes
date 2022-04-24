
import yaml

def main():
    with open("value_indentation.yaml", encoding="utf-8") as f:
        data = yaml.load(f, Loader=yaml.Loader)
    print(data)


if __name__ == "__main__":
    main()