"""
API routes for the Claude - Docling API Wrapper.
"""
import logging
import time
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from docling_wrapper.api.models import (
    ConversionRequest,
    ConversionResponse,
    ErrorResponse,
    SourceType,
)
from docling_wrapper.services.html_converter import (
    convert_html_source_to_markdown,
    convert_html_url_to_markdown,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Conversion"])


@router.post(
    "/convert",
    response_model=ConversionResponse,
    responses={
        200: {"model": ConversionResponse},
        400: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)
async def convert_document(request: Request, conversion_request: ConversionRequest):
    """
    Convert a document to Markdown.

    Currently supports:
    - HTML from URL
    - HTML source content

    PDF support will be added in a future update.
    """
    start_time = time.time()
    logger.info(f"Received conversion request of type: {conversion_request.type}")

    try:
        # Extract options
        options = conversion_request.options or {}
        headers = options.headers if options and hasattr(options, "headers") else None

        # Process based on source type
        if conversion_request.type == SourceType.HTML_URL:
            markdown_content, metadata = await convert_html_url_to_markdown(
                conversion_request.source, headers
            )
        elif conversion_request.type == SourceType.HTML_SOURCE:
            markdown_content, metadata = await convert_html_source_to_markdown(
                conversion_request.source
            )
        elif conversion_request.type == SourceType.PDF:
            # PDF support not implemented yet
            raise NotImplementedError("PDF conversion is not yet implemented")
        else:
            raise ValueError(f"Unsupported source type: {conversion_request.type}")

        # Create response
        response = ConversionResponse(
            success=True,
            markdown=markdown_content,
            metadata=metadata if options and options.include_metadata else None,
        )

        logger.info(
            f"Conversion completed successfully in {int((time.time() - start_time) * 1000)}ms"
        )
        return response

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                success=False,
                error="Validation error",
                details={"message": str(e)},
            ).dict(),
        )
    except NotImplementedError as e:
        logger.warning(f"Not implemented: {str(e)}")
        return JSONResponse(
            status_code=501,
            content=ErrorResponse(
                success=False,
                error="Not implemented",
                details={"message": str(e)},
            ).dict(),
        )
    except Exception as e:
        logger.exception(f"Error during conversion: {str(e)}")
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                success=False,
                error="Internal server error",
                details={"message": str(e)},
            ).dict(),
        )
