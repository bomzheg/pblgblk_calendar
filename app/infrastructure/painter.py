import calendar
from datetime import date
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.table import Table


class CalendarPainterImpl:
    """
    sorry code bellow is LLM-slop, but it works, so...
    """

    def __init__(  # noqa: PLR0913
        self,
        header_color: str = "#2E4057",
        weekday_color: str = "#34495E",
        default_cell_color: str = "white",
        highlight_color: str = "#E74C3C",
        title_fontsize: int = 16,
        weekday_fontsize: int = 12,
        day_fontsize: int = 11,
        figsize: tuple = (10, 8),
        dpi: int = 300,
    ) -> None:
        """
        header_color: Color for the month/year header
        weekday_color: Color for weekday headers (Mon-Sun)
        default_cell_color: Background color for regular dates
        highlight_color: Background color for highlighted dates
        title_fontsize: Font size for month/year title
        weekday_fontsize: Font size for weekday headers
        day_fontsize: Font size for day numbers
        figsize: Figure size (width, height) in inches
        dpi: Dots per inch for output image quality
        """
        self.header_color = header_color
        self.weekday_color = weekday_color
        self.default_cell_color = default_cell_color
        self.highlight_color = highlight_color
        self.title_fontsize = title_fontsize
        self.weekday_fontsize = weekday_fontsize
        self.day_fontsize = day_fontsize
        self.figsize = figsize
        self.dpi = dpi
        self.weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def _prepare_calendar_data(
        self, year: int, month: int, highlight_dates: list[date]
    ) -> tuple[list[list[str]], list[list[str]]]:
        cal_matrix = calendar.monthcalendar(year, month)
        highlight_dates_set = set(highlight_dates)

        table_data: list[list[str]] = [self.weekdays.copy()]
        cell_colors: list[list[str]] = [[self.weekday_color] * 7]

        # Process each week
        for week in cal_matrix:
            week_data: list[str] = []
            week_colors: list[str] = []

            for day in week:
                if day == 0:
                    week_data.append("")
                    week_colors.append(self.default_cell_color)
                else:
                    week_data.append(str(day))
                    current_date = date(year, month, day)

                    if current_date in highlight_dates_set:
                        week_colors.append(self.highlight_color)
                    else:
                        week_colors.append(self.default_cell_color)

            table_data.append(week_data)
            cell_colors.append(week_colors)

        return table_data, cell_colors

    def _create_figure(self, year: int, month: int) -> tuple[plt.Figure, plt.Axes]:
        fig, ax = plt.subplots(figsize=self.figsize)

        # Hide axes
        ax.axis("tight")
        ax.axis("off")

        # Set title
        month_name = calendar.month_name[month]
        ax.set_title(
            f"{month_name} {year}",
            fontsize=self.title_fontsize,
            pad=30,
            color=self.header_color,
            fontweight="bold",
        )

        return fig, ax

    def _create_calendar_table(
        self, ax: plt.Axes, table_data: list[list[str]], cell_colors: list[list[str]]
    ) -> Table:
        """Create the calendar table in the matplotlib figure."""
        table = ax.table(
            cellText=table_data,
            cellColours=cell_colors,
            cellLoc="center",
            loc="center",
            # left, bottom, width, height
            bbox=[0.0, 0.0, 1, 0.9],  # type: ignore[arg-type]
        )

        # Style the table
        table.auto_set_font_size(value=False)

        # Apply different font sizes for headers vs days
        for (row, _col), cell in table.get_celld().items():
            cell.set_height(0.12)  # Adjust cell height

            if row == 0:  # Header row (weekdays)
                cell.set_fontsize(self.weekday_fontsize)
                cell.set_text_props(weight="bold", color="white")
                cell.set_edgecolor("white")
                cell.set_linewidth(1.5)
            else:  # Day cells
                cell.set_fontsize(self.day_fontsize)
                cell.set_text_props(color="black")
                cell.set_edgecolor("#EAEDED")
                cell.set_linewidth(0.5)

        return table

    def paint(
        self, year: int, month: int, dates: list[date], return_format: str = "jpg"
    ) -> BytesIO:
        """
        Create a calendar image with highlighted dates.

        Args:
            year: Year (e.g., 2025)
            month: Month [1-12]
            dates: list of dates to be colored red
            return_format: Output format - 'jpg' or 'png'

        Returns:
            BytesIO: Image data in memory

        Raises:
            ValueError: If month is not in [1-12] or return_format is invalid
        """
        # Validate inputs
        if not 1 <= month <= 12:  # noqa: PLR2004
            raise ValueError(f"Month must be between 1 and 12, got {month}")

        # Prepare data
        table_data, cell_colors = self._prepare_calendar_data(year, month, dates)

        # Create figure
        fig, ax = self._create_figure(year, month)

        # Create table
        self._create_calendar_table(ax, table_data, cell_colors)

        # Adjust layout
        plt.tight_layout(pad=3.0)

        # Save to BytesIO
        img_data = BytesIO()

        fig.savefig(
            img_data, format=return_format, dpi=self.dpi, bbox_inches="tight", facecolor="white"
        )

        plt.close(fig)
        img_data.seek(0)
        return img_data


if __name__ == "__main__":
    # Example 1: Using the SimpleCalendarPainter
    simple_painter = CalendarPainterImpl()

    # Create some test dates
    test_dates = [
        date(2024, 3, 5),  # Highlighted in red
        date(2024, 3, 15),  # Highlighted in red
        date(2024, 3, 25),  # Highlighted in red
    ]

    # Get image as BytesIO
    image_data = simple_painter.paint(2024, 3, test_dates)

    # Save to file
    with open("simple_calendar.jpg", "wb") as f:  # noqa: PTH123
        f.write(image_data.getbuffer())
