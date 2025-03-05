#!/usr/bin/env python3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math
import argparse

def get_page_label(page_num):
    """
    Convert page numbers to descriptive labels.
    """
    content_num = page_num
        
        
    return f"Content {content_num}"

def calculate_page_order(total_pages):
    """
    Calculate the order of pages for the booklet layout.
    Each A4 sheet will contain 4 A5 pages (2 on each side when folded).
    
    For a booklet, pages should be arranged so that when printed double-sided
    and folded, they appear in the correct order from start to finish.
    
    The cover should be on the right side of the first sheet, so when folded
    it becomes the front of the booklet.
    """
    # Add empty pages if needed to make total divisible by 4
    if total_pages % 4 != 0:
        total_pages += (4 - (total_pages % 4))
    
    
    # Calculate number of sheets needed (each sheet has 4 pages)
    num_sheets = total_pages // 4
    
    # Create the page ordering
    page_order = []
    
    left_counter = 1
    right_counter = total_pages
    for sheet in range(num_sheets):
        page_order.append((right_counter, left_counter))
        page_order.append((left_counter + 1, right_counter - 1))
        left_counter += 2
        right_counter -= 2
    
    return page_order

def create_layout_guide(total_pages):
    """
    Create a PDF guide showing how to arrange the pages.
    """
    # Use landscape orientation by swapping width and height
    height, width = A4  # A4 is originally in portrait, so we swap dimensions
    c = canvas.Canvas("booklet.pdf"	, pagesize=(width, height))
    
    # Calculate page ordering
    page_order = calculate_page_order(total_pages)
    
    # Create a page for each sheet (front and back)
    for i, (left_page, right_page) in enumerate(page_order):
        # Draw sheet outline
        c.rect(1*cm, 1*cm, width-2*cm, height-2*cm)
        
        # Draw fold line
        c.setDash(6, 3)
        c.line(width/2, 1*cm, width/2, height-1*cm)
        c.setDash(1, 0)
        
        # Add sheet number and side information
        c.setFont("Helvetica", 16)
        side = "Front" if i % 2 == 0 else "Back"
        sheet_num = i//2 + 1
        total_sheets = len(page_order)//2
        c.drawString(2*cm, height-1.5*cm, f"Sheet {sheet_num} of {total_sheets} - {side}")
        
        # Get descriptive labels for pages
        left_label = get_page_label(left_page)
        right_label = get_page_label(right_page)
        
        # Draw page labels with better positioning for landscape
        c.setFont("Helvetica", 24)  # Slightly smaller for longer labels
        # Calculate positions for better spacing in landscape mode
        text_y = height/2 - 0.5*cm
        
        # Left side
        c.drawString(width/4 - 3*cm, text_y, left_label)
        # Right side
        c.drawString(3*width/4 - 3*cm, text_y, right_label)
        
        # Add page numbers in smaller font below labels
        c.setFont("Helvetica", 12)
        c.drawString(width/4 - 3*cm, text_y - 1*cm, f"(Page {left_page})")
        c.drawString(3*width/4 - 3*cm, text_y - 1*cm, f"(Page {right_page})")
        
        # Add fold instructions
        c.setFont("Helvetica", 12)
        if i % 2 == 0:
            instructions = [
                "1. Print all front sides first",
                "2. Reinsert the printed pages to print the back sides",
                "3. Make sure to maintain the same orientation"
            ]
        else:
            instructions = [
                "1. After printing both sides",
                "2. Fold along the dotted line",
                "3. Stack sheets in order (Sheet 1 outermost)"
            ]
        
        # Draw instructions with proper spacing
        for idx, line in enumerate(instructions):
            c.drawString(2*cm, 2*cm + (idx * 0.6*cm), line)
        
        c.showPage()
    
    c.save()

def main():
    parser = argparse.ArgumentParser(description='Create a booklet layout guide')
    parser.add_argument('total_pages', type=int, help='Total number of content pages')
    args = parser.parse_args()
    
    create_layout_guide(args.total_pages)
    print(f"Total sheets needed: {math.ceil(args.total_pages/4)}")

if __name__ == "__main__":
    main() 