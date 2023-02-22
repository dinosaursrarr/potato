import json

from .imagemap import Handler


def noop_callback(current_url: str, new_url: str) -> None:
    pass


def test_include_url(tmp_path):
    content = open('pedigree/imagemap.html').read()
    url = 'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=2602&depth=8&showjaar=0'
    output_dir = tmp_path / "name"
    output_dir.mkdir()

    Handler(output_dir).handle(content, url, noop_callback)

    with open(output_dir / "2602.json") as f:
        result = json.load(f)
        assert result['url'] == url


def test_extract_name(tmp_path):
    content = open('pedigree/imagemap.html').read()
    url = 'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=2602&depth=8&showjaar=0'
    output_dir = tmp_path / "name"
    output_dir.mkdir()

    Handler(output_dir).handle(content, url, noop_callback)

    with open(output_dir / "2602.json") as f:
        result = json.load(f)
        assert result['name'] == 'DRAYTON'


def test_extract_year(tmp_path):
    content = open('pedigree/imagemap.html').read()
    url = 'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=2602&depth=8&showjaar=0'
    output_dir = tmp_path / "name"
    output_dir.mkdir()

    Handler(output_dir).handle(content, url, noop_callback)

    with open(output_dir / "2602.json") as f:
        result = json.load(f)
        assert result['year_of_introduction'] == 1976


def test_extract_parentage(tmp_path):
    content = open('pedigree/imagemap.html').read()
    url = 'https://www.plantbreeding.wur.nl/PotatoPedigree/pedigree_imagemap.php?id=2602&depth=8&showjaar=0'
    output_dir = tmp_path / "name"
    output_dir.mkdir()

    Handler(output_dir).handle(content, url, noop_callback)

    with open(output_dir / "2602.json") as f:
        result = json.load(f)
        assert result['parentage'] == [
            {
                "name": "DRAYTON",
                "coordinates": [0, 2555, 40, 2565],
                "year_of_introduction": 1976,
            },
            {
                "name": "RED KING EDWARD",
                "coordinates": [100, 1275, 140, 1285],
                "year_of_introduction": 1916,
            },
            {
                "name": "MARIS PIPER",
                "coordinates": [100, 3835, 140, 3845],
                "year_of_introduction": 1963,
            },
            {
                "name": "KING EDWARD",
                "coordinates": [200, 635, 240, 645],
                "year_of_introduction": 1902,
            },
            {
                "name": "Y 22/6",
                "coordinates": [200, 3195, 240, 3205],
            },
            {
                "name": "1ARRAN CAIRN x HERALD",
                "coordinates": [200, 4475, 240, 4485],
                "year_of_introduction": 1963,
            },
            {
                "name": "MAGNUM BONUM",
                "coordinates": [300, 315, 340, 325],
                "year_of_introduction": 1876,
            },
            {
                "name": "BEAUTY OF HEBRON",
                "coordinates": [300, 955, 340, 965],
                "year_of_introduction": 1878,
            },
            {
                "name": "H 4/31",
                "coordinates": [300, 2875, 340, 2885],
            },
            {
                "name": "ULSTER KNIGHT",
                "coordinates": [300, 3515, 340, 3525],
                "year_of_introduction": 1954,
            },
            {
                "name": "ARRAN CAIRN",
                "coordinates": [300, 4155, 340, 4165],
                "year_of_introduction": 1930,
            },
            {
                "name": "HERALD",
                "coordinates": [300, 4795, 340, 4805],
                "year_of_introduction": 1928,
            },
            {
                "name": "EARLY ROSE",
                "coordinates": [400, 155, 440, 165],
                "year_of_introduction": 1867,
            },
            {
                "name": "PATERSON'S VICTORIA",
                "coordinates": [400, 475, 440, 485],
                "year_of_introduction": 1856,
            },
            {
                "name": "GARNET CHILI",
                "coordinates": [400, 795, 440, 805],
                "year_of_introduction": 1857,
            },
            {
                "name": "GARNET CHILI",
                "coordinates": [400, 1115, 440, 1125],
                "year_of_introduction": 1857,
            },
            {
                "name": "CPC 1673 (adg)",
                "coordinates": [400, 2715, 440, 2725],
            },
            {
                "name": "CPC 1673 (adg)",
                "coordinates": [400, 3035, 440, 3045],
            },
            {
                "name": "CLARKE 736",
                "coordinates": [400, 3355, 440, 3365],
            },
            {
                "name": "CRAIGS DEFIANCE",
                "coordinates": [400, 3675, 440, 3685],
                "year_of_introduction": 1938,
            },
            {
                "name": "MAY QUEEN",
                "coordinates": [400, 3995, 440, 4005],
                "year_of_introduction": 1890,
            },
            {
                "name": "PEPO",
                "coordinates": [400, 4315, 440, 4325],
            },
            {
                "name": "MAJESTIC",
                "coordinates": [400, 4635, 440, 4645],
                "year_of_introduction": 1911,
            },
            {
                "name": "ABUNDANCE",
                "coordinates": [400, 4955, 440, 4965],
                "year_of_introduction": 1886,
            },
            {
                "name": "GARNET CHILI",
                "coordinates": [500, 75, 540, 85],
                "year_of_introduction": 1857,
            },
            {
                "name": "FLUKE",
                "coordinates": [500, 395, 540, 405],
            },
            {
                "name": "ROUGH PURPLE CHILI",
                "coordinates": [500, 715, 540, 725],
                "year_of_introduction": 1851,
            },
            {
                "name": "ROUGH PURPLE CHILI",
                "coordinates": [500, 1035, 540, 1045],
                "year_of_introduction": 1851,
            },
            {
                "name": "BALLYDOON",
                "coordinates": [500, 3275, 540, 3285],
                "year_of_introduction": 1931,
            },
            {
                "name": "KATAHDIN",
                "coordinates": [500, 3435, 540, 3445],
                "year_of_introduction": 1932,
            },
            {
                "name": "EPICURE",
                "coordinates": [500, 3595, 540, 3605],
                "year_of_introduction": 1897,
            },
            {
                "name": "PEPO",
                "coordinates": [500, 3755, 540, 3765],
            },
            {
                "name": "unknown",
                "coordinates": [500, 3915, 540, 3925],
            },
            {
                "name": "TASSO",
                "coordinates": [500, 4235, 540, 4245],
            },
            {
                "name": "63/85",
                "coordinates": [500, 4395, 540, 4405],
            },
            {
                "name": "BRITISH QUEEN",
                "coordinates": [500, 4555, 540, 4565],
            },
            {
                "name": "MAGNUM BONUM",
                "coordinates": [500, 4875, 540, 4885],
                "year_of_introduction": 1876,
            },
            {
                "name": "FOX'S SEEDLING",
                "coordinates": [500, 5035, 540, 5045],
                "year_of_introduction": 1820,
            },
            {
                "name": "ROUGH PURPLE CHILI",
                "coordinates": [600, 35, 640, 45],
                "year_of_introduction": 1851,
            },
            {
                "name": "COLOSSAL synonym (fra)",
                "coordinates": [600, 355, 640, 365],
            },
            {
                "name": "unknown",
                "coordinates": [600, 675, 640, 685],
            },
            {
                "name": "unknown",
                "coordinates": [600, 995, 640, 1005],
            },
            {
                "name": "HERALD",
                "coordinates": [600, 3235, 640, 3245],
                "year_of_introduction": 1928,
            },
            {
                "name": "BRITISH QUEEN",
                "coordinates": [600, 3315, 640, 3325],
            },
            {
                "name": "USDA 40568",
                "coordinates": [600, 3395, 640, 3405],
            },
            {
                "name": "USDA 24642",
                "coordinates": [600, 3475, 640, 3485],
            },
            {
                "name": "MAGNUM BONUM",
                "coordinates": [600, 3555, 640, 3565],
                "year_of_introduction": 1876,
            },
            {
                "name": "EARLY REGENT",
                "coordinates": [600, 3635, 640, 3645],
                "year_of_introduction": 1882,
            },
            {
                "name": "TASSO",
                "coordinates": [600, 3715, 640, 3725],
            },
            {
                "name": "63/85",
                "coordinates": [600, 3795, 640, 3805],
            },
            {
                "name": "UP TO DATE",
                "coordinates": [600, 4515, 640, 4525],
                "year_of_introduction": 1894,
            },
            {
                "name": "EARLY ROSE",
                "coordinates": [600, 4835, 640, 4845],
                "year_of_introduction": 1867,
            },
            {
                "name": "PATERSON'S VICTORIA",
                "coordinates": [600, 4915, 640, 4925],
                "year_of_introduction": 1856,
            },
            {
                "name": "OLD BLUE DON seedling",
                "coordinates": [600, 4995, 640, 5005],
            },
            {
                "name": "unknown",
                "coordinates": [700, 15, 740, 25],
            },
            {
                "name": "MAJESTIC",
                "coordinates": [700, 3215, 740, 3225],
                "year_of_introduction": 1911,
            },
            {
                "name": "ABUNDANCE",
                "coordinates": [700, 3255, 740, 3265],
                "year_of_introduction": 1886,
            },
            {
                "name": "UP TO DATE",
                "coordinates": [700, 3295, 740, 3305],
                "year_of_introduction": 1894,
            },
            {
                "name": "BUSOLA",
                "coordinates": [700, 3375, 740, 3385],
            },
            {
                "name": "RURAL NEW YORKER NO. 2",
                "coordinates": [700, 3415, 740, 3425],
                "year_of_introduction": 1888,
            },
            {
                "name": "WHITE ROSE",
                "coordinates": [700, 3455, 740, 3465],
                "year_of_introduction": 1871,
            },
            {
                "name": "SUTTON'S FLOURBALL",
                "coordinates": [700, 3495, 740, 3505],
                "year_of_introduction": 1870,
            },
            {
                "name": "EARLY ROSE",
                "coordinates": [700, 3535, 740, 3545],
                "year_of_introduction": 1867,
            },
            {
                "name": "PATERSON'S VICTORIA",
                "coordinates": [700, 3575, 740, 3585],
                "year_of_introduction": 1856,
            },
            {
                "name": "EARLY ROSE",
                "coordinates": [700, 3615, 740, 3625],
                "year_of_introduction": 1867,
            },
            {
                "name": "PATERSON'S VICTORIA",
                "coordinates": [700, 3655, 740, 3665],
                "year_of_introduction": 1856,
            },
            {
                "name": "PATERSON'S VICTORIA",
                "coordinates": [700, 4495, 740, 4505],
                "year_of_introduction": 1856,
            },
            {
                "name": "BLUE DON",
                "coordinates": [700, 4535, 740, 4545],
                "year_of_introduction": 1894,
            },
            {
                "name": "GARNET CHILI",
                "coordinates": [700, 4815, 740, 4825],
                "year_of_introduction": 1857,
            },
            {
                "name": "FLUKE",
                "coordinates": [700, 4895, 740, 4905],
            },
            {
                "name": "BRITISH QUEEN seedling",
                "coordinates": [800, 3205, 840, 3215],
            },
            {
                "name": "MAGNUM BONUM",
                "coordinates": [800, 3245, 840, 3255],
            },
            {
                "name": "FOX'S SEEDLING",
                "coordinates": [800, 3265, 840, 3275],
            },
            {
                "name": "PATERSON'S VICTORIA",
                "coordinates": [800, 3285, 840, 3295],
            },
            {
                "name": "BLUE DON",
                "coordinates": [800, 3305, 840, 3315],
            },
            {
                "name": "FURSTIN HATZFELD",
                "coordinates": [800, 3365, 840, 3375],
            },
            {
                "name": "ALABASTER",
                "coordinates": [800, 3385, 840, 3395],
            },
            {
                "name": "unknown",
                "coordinates": [800, 3405, 840, 3415],
            },
            {
                "name": "JACKSON seedling",
                "coordinates": [800, 3445, 840, 3455],
            },
            {
                "name": "unknown",
                "coordinates": [800, 3485, 840, 3495],
            },
            {
                "name": "GARNET CHILI seedling",
                "coordinates": [800, 3525, 840, 3535],
            },
            {
                "name": "FLUKE seedling",
                "coordinates": [800, 3565, 840, 3575],
            },
            {
                "name": "GARNET CHILI seedling",
                "coordinates": [800, 3605, 840, 3615],
            },
            {
                "name": "FLUKE seedling",
                "coordinates": [800, 3645, 840, 3655],
            },
            {
                "name": "FLUKE seedling",
                "coordinates": [800, 4485, 840, 4495],
            },
            {
                "name": "unknown",
                "coordinates": [800, 4525, 840, 4535],
            },
            {
                "name": "ROUGH PURPLE CHILI seedling",
                "coordinates": [800, 4805, 840, 4815],
            },
            {
                "name": "COLOSSAL synonym (fra)",
                "coordinates": [800, 4885, 840, 4895],
            },
        ]
