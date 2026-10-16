"""
DeveloperOS Data Conversion Suite - Interactive Application
"""

import streamlit as st
from core.converter import convert_and_format_json
from ui.components import render_suite_header, render_suite_footer, render_main_promotional_banner

st.set_page_config(
    page_title="DeveloperOS - Data Convert Suite",
    page_icon="🔄",
    layout="wide",
)


def main():
    render_suite_header(
        title="JSON Prettifier, Formatter & Validator",
        description="Format, validate syntax, and inspect structured metrics for JSON documents with zero network transmission.",
    )

    sample_json = '{"project":"DeveloperOS","version":"1.0.0","tools":["meta-tags","curl-parser","hasher"],"config":{"ephemeral":true}}'

    raw_input = st.text_area("Input JSON:", value=sample_json, height=140)

    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        indent = st.slider("Indentation Spaces", 2, 8, 2)
    with col_ctrl2:
        sort_keys = st.checkbox("Sort Dictionary Keys Alphabetically", value=False)

    if raw_input:
        success, output, metrics = convert_and_format_json(raw_input, indent=indent, sort_keys=sort_keys)

        if success:
            st.success("JSON Syntax Valid!")
            col_m1, col_m2, col_m3 = st.columns(3)
            col_m1.metric("Size", f"{metrics['byte_size']} bytes")
            col_m2.metric("Items / Keys", metrics["item_count"])
            col_m3.metric("Root Type", "Array" if metrics["is_array"] else "Object")

            st.subheader("Formatted Output")
            st.code(output, language="json")
        else:
            st.error(output)

    render_main_promotional_banner()
    render_suite_footer()


if __name__ == "__main__":
    main()
