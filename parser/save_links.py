import petshop_parser

url = 'https://www.petshop.ru/catalog/'
get_links = petshop_parser.LinksPetshop(url)
get_product = get_links.product_links()