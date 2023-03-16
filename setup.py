from setuptools import setup, find_packages

setup(
    name='AIChatMe_BOT',
    version='1.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aichatme_bot = AIChatMe_BOT:main'
        ]
    },
    install_requires=[
        'requests',
        'websocket-client',
        'spotipy',
        'google-auth',
        'google-auth-oauthlib',
        'google-auth-httplib2',
        'google-api-python-client',
        'googletrans==4.0.0-rc1'
    ],
    include_package_data=True
)
