"""Normalize a transparent boxed-resource contents layer to the AMJ masu opening plane.

Image generation supplies the subject/style. This tool removes low-alpha
background residue, crops the visible contents, and deterministically projects
that crop onto the registered diamond-like contents plane. Final placement,
masking and rim occlusion against the wooden masu remain manual.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


DEFAULT_QUAD = (
    (0.50, 0.18),  # source top-left -> visual rear corner
    (0.88, 0.50),  # source top-right -> visual right corner
    (0.50, 0.82),  # source bottom-right -> visual front corner
    (0.12, 0.50),  # source bottom-left -> visual left corner
)


def _solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    """Solve Ax=b using Gaussian elimination with partial pivoting."""
    n = len(b)
    matrix = [row[:] + [b[i]] for i, row in enumerate(a)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(matrix[row][col]))
        if abs(matrix[pivot][col]) < 1e-12:
            raise ValueError("degenerate perspective quadrilateral")
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]

        divisor = matrix[col][col]
        matrix[col] = [value / divisor for value in matrix[col]]

        for row in range(n):
            if row == col:
                continue
            factor = matrix[row][col]
            if factor:
                matrix[row] = [
                    matrix[row][i] - factor * matrix[col][i]
                    for i in range(n + 1)
                ]
    return [matrix[i][n] for i in range(n)]


def _perspective_coefficients(
    destination: list[tuple[float, float]],
    source: list[tuple[float, float]],
) -> tuple[float, ...]:
    """Return Pillow output->input perspective coefficients for four point pairs."""
    equations: list[list[float]] = []
    answers: list[float] = []

    # Pillow maps each output pixel back into the input:
    # x_s = (a*x_d + b*y_d + c) / (g*x_d + h*y_d + 1)
    # y_s = (d*x_d + e*y_d + f) / (g*x_d + h*y_d + 1)
    for (xd, yd), (xs, ys) in zip(destination, source):
        equations.append(
            [xd, yd, 1.0, 0.0, 0.0, 0.0, -xs * xd, -xs * yd]
        )
        answers.append(xs)
        equations.append(
            [0.0, 0.0, 0.0, xd, yd, 1.0, -ys * xd, -ys * yd]
        )
        answers.append(ys)

    return tuple(_solve_linear(equations, answers))


def _clean_alpha(image: Image.Image, cutoff: int) -> Image.Image:
    """Zero low-alpha pixels including hidden RGB to prevent dark resampling halos."""
    rgba = image.convert("RGBA")
    data = bytearray(rgba.tobytes())
    for index in range(0, len(data), 4):
        if data[index + 3] < cutoff:
            data[index] = 0
            data[index + 1] = 0
            data[index + 2] = 0
            data[index + 3] = 0
    return Image.frombytes("RGBA", rgba.size, bytes(data))


def normalize(
    source: Path,
    output: Path,
    *,
    canvas: int = 1024,
    alpha_cutoff: int = 40,
    quad: tuple[tuple[float, float], ...] = DEFAULT_QUAD,
) -> None:
    with Image.open(source) as opened:
        opened.load()
        image = _clean_alpha(opened, alpha_cutoff)

    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        raise ValueError("source contains no visible alpha after cleanup")

    crop = image.crop(bbox)
    source_width, source_height = crop.size
    source_points = [
        (0.0, 0.0),
        (source_width - 1.0, 0.0),
        (source_width - 1.0, source_height - 1.0),
        (0.0, source_height - 1.0),
    ]
    destination_points = [
        (x * canvas, y * canvas)
        for x, y in quad
    ]
    coefficients = _perspective_coefficients(
        destination_points,
        source_points,
    )

    projected = crop.transform(
        (canvas, canvas),
        Image.Transform.PERSPECTIVE,
        coefficients,
        resample=Image.Resampling.BICUBIC,
        fillcolor=(0, 0, 0, 0),
    )
    projected = _clean_alpha(projected, 8)

    output.parent.mkdir(parents=True, exist_ok=True)
    projected.save(output, format="PNG")


def _parse_quad(value: str) -> tuple[tuple[float, float], ...]:
    points = []
    for item in value.split(";"):
        x, y = item.split(",", 1)
        points.append((float(x), float(y)))

    if len(points) != 4:
        raise argparse.ArgumentTypeError(
            "quad must contain four x,y pairs"
        )
    if any(
        not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0)
        for x, y in points
    ):
        raise argparse.ArgumentTypeError(
            "quad coordinates must be normalized 0..1"
        )
    return tuple(points)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--canvas", type=int, default=1024)
    parser.add_argument("--alpha-cutoff", type=int, default=40)
    parser.add_argument(
        "--quad",
        type=_parse_quad,
        default=DEFAULT_QUAD,
        help=(
            "normalized TL;TR;BR;BL destination points, e.g. "
            "0.50,0.18;0.88,0.50;0.50,0.82;0.12,0.50"
        ),
    )
    args = parser.parse_args()

    if args.canvas <= 0:
        parser.error("--canvas must be positive")
    if not 0 <= args.alpha_cutoff <= 255:
        parser.error("--alpha-cutoff must be 0..255")

    normalize(
        args.source,
        args.output,
        canvas=args.canvas,
        alpha_cutoff=args.alpha_cutoff,
        quad=args.quad,
    )


if __name__ == "__main__":
    main()
