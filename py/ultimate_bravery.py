from py import assign_build, generate_data, generate_html, generate_types


def main():
    generate_data.main()
    generate_types.main()
    assign_build.main()
    generate_html.main()

if __name__ == "__main__":
    main()