#! /usr/bin/env python3

from wind.base.server import create_app

def main():
   app = create_app()
   app.run()
