# booklet project

this project aims at helping desining and organising a booklet of A5 pages from on A4 pages in portrait mode, folded in half.

The order of the pages needs to be calculated so when pages are printed and folded together the content is in the expected order.

The project is a python script that takes as input the number of pages in of the content, and will create a guide that illustrates how to reorganise the original A4 in portrait mode content so it will be ordered as expected when folded and put together.

For example, to generate a booklet with 14 pages, run this

`python booklet.py 14`

the output will be a pdf with 16 pages (it's always a multiple of 4), that shows you how pages will be reorganised once folded.