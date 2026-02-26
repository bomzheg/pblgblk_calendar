from datetime import date
from typing import Any

from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.api.internal import StyleWidget
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope
from aiogram_dialog.widgets.kbd.calendar_kbd import (
    CalendarDaysView,
    CalendarMonthView,
    CalendarScopeView,
    CalendarYearsView,
    raw_from_date,
)
from aiogram_dialog.widgets.style import Style


class BusyCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        """
        Calendar scopes view initializer.

        Override this method customize how calendar is rendered.
        You can either set Text widgets for buttons in default views or
        create own implementation of views
        """
        return {
            CalendarScope.DAYS: BusyCalendarDays(self._item_callback_data),
            CalendarScope.MONTHS: CalendarMonthView(self._item_callback_data),
            CalendarScope.YEARS: CalendarYearsView(self._item_callback_data),
        }


BUSY_STYLE: StyleWidget = Style(style="danger")


class BusyCalendarDays(CalendarDaysView):
    async def _render_date_button(
        self,
        selected_date: date,
        today: date,
        data: dict[str, Any],
        manager: DialogManager,
    ) -> InlineKeyboardButton:
        current_data = {
            "date": selected_date,
            "data": data,
        }
        if selected_date in data.get("busy", []):
            text = self.date_text
            style = BUSY_STYLE
        elif selected_date == today:
            text = self.today_text
            style = self.today_style
        else:
            text = self.date_text
            style = self.date_style
        raw_date = raw_from_date(selected_date)
        return InlineKeyboardButton(
            text=await text.render_text(
                current_data,
                manager,
            ),
            style=await style.render_style(current_data, manager),
            callback_data=self.callback_generator(str(raw_date)),
            icon_custom_emoji_id=await style.render_emoji(
                current_data,
                manager,
            ),
        )
