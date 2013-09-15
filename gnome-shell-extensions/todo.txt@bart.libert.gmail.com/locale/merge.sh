#!/bin/sh
for lang in en nl; do
	msgmerge -U po/${lang}.po messages.pot;
done
