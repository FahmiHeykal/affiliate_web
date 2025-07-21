def site_settings(request):
    return {
        'SITE_NAME': 'Affiliate Web',
        'SITE_DESCRIPTION': 'Platform Afiliasi Produk Terbaik',
        'SITE_AUTHOR': 'Affiliate Team',
        'SITE_URL': request.build_absolute_uri('/'),
        'CURRENT_YEAR': '2023',
    }