#!/usr/bin/env python

import boto3
import json

class Thing():
    def __init__(self, name):
        self.client = boto3.client('iot')
        self.name = name
        self.arn = ''

    def create(self):
        assert self.exists() == False, "Thing already exists"
        print("Creating a Thing in AWS IoT Core.")
        result = self.client.create_thing(thingName=self.name)
        self.arn = result['thingArn']

    def delete(self):
        assert self.exists() == True, "Thing does not exist"
        principals = self.list_principals()
        for principal in principals:
            self.detach_principal(principal)
        print(f"Deleting a Thing in AWS IoT Core named {self.name}.")
        self.client.delete_thing(thingName=self.name)

    def exists(self):
        list_of_things = self.client.list_things()['things']
        return any(thing['thingName'] == self.name for thing in list_of_things)

    def attach_principal(self, arn):
        assert self.exists() == True, "Thing does not exist"
        print(f"Attaching principal with ARN {arn} to Thing named {self.name}.")
        self.client.attach_thing_principal(thingName=self.name,
            principal=arn)


    def detach_principal(self, arn):
        assert self.exists() == True, "Thing does not exist"
        print(f"Detaching principal with ARN {arn} to Thing named {self.name}.")
        self.client.detach_thing_principal(thingName=self.name,
            principal=arn)


    def list_principals(self):
        assert self.exists() == True, "Thing does not exist"
        principals = self.client.list_thing_principals(thingName=self.name)
        principals = principals['principals']
        return principals
