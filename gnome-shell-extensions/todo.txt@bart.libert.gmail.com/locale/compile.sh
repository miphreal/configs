#!/bin/sh
for lang in en nl; do
	msgfmt po/${lang}.po -o ${lang}/LC_MESSAGES/todotxt.mo
done
