var _vendor = {
        'Acer': '0502',
        'ASUS': '0b05',
        'Dell': '413c',
        'Foxconn': '0489',
        'Fujitsu': '04c5',
        'Fujitsu Toshiba': '04c5',
        'Garmin-Asus': '091e',
        'Google': '18d1',
        'Haier': '201E',
        'Hisense': '109b',
        'HTC': '0bb4',
        'Huawei': '12d1',
        'K-Touch': '24e3',
        'KT Tech': '2116',
        'Kyocera': '0482',
        'Lenovo': '17ef',
        'LG': '1004',
        'Motorola': '22b8',
        'MTK': '0e8d',
        'NEC': '0409',
        'Nook': '2080',
        'Nvidia': '0955',
        'OTGV': '2257',
        'Pantech': '10a9',
        'Pegatron': '1d4d',
        'Philips': '0471',
        'PMC-Sierra': '04da',
        'Qualcomm': '05c6',
        'SK Telesys': '1f53',
        'Samsung': '04e8',
        'Sharp': '04dd',
        'Sony': '054c',
        'Sony Ericsson': '0fce',
        'Teleepoch': '2340',
        'Toshiba': '0930',
        'ZTE': '19d2'
    }
    for(var vendor_key in _vendor){
        console.log('SUBSYSTEM=="usb", ATTR{idVendor}=="%s", MODE="0666", GROUP="plugdev"', _vendor[vendor_key])
    }