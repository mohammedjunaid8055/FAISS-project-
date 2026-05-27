#!/usr/bin/env bash
# Start the Streamlit application with custom network overrides for Render
streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false
