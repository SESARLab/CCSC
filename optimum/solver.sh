#!/bin/bash

for filename in ../dataset/share/*
do
  destination=${filename}.result
  glpsol -m deploy.mod -d $filename > $destination
done

for filename in ../dataset/fitting/*
do
  destination=${filename}.result
  glpsol -m deploy.mod -d $filename > $destination
done

for filename in ../dataset/average/*
do
  destination=${filename}.result
  glpsol -m deploy.mod -d $filename > $destination
done

