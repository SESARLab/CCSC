#!/bin/bash

for filename in dataset/shareProfile/*
do
  destination=${filename}.result
  glpsol -m deploy.mod -d $filename > $destination
done

for filename in dataset/fittingProfile/*
do
  destination=${filename}.result
  glpsol -m deploy.mod -d $filename > $destination
done

for filename in dataset/averageProfile/*
do
  destination=${filename}.result
  glpsol -m deploy.mod -d $filename > $destination
done

