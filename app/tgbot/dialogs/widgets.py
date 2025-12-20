from datetime import date
from time import mktime
from typing import Any

from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar, CalendarScope
from aiogram_dialog.widgets.kbd.calendar_kbd import CalendarScopeView, CalendarDaysView, CalendarMonthView, \
    CalendarYearsView
from aiogram_dialog.widgets.text import Text, Format, Const


class ViewCalendar(Calendar):
    def _init_views(self) -> dict[CalendarScope, CalendarScopeView]:
        """
        Calendar scopes view initializer.

        Override this method customize how calendar is rendered.
        You can either set Text widgets for buttons in default views or
        create own implementation of views
        """
        return {
            CalendarScope.DAYS:
                ViewCalendarDays(self._item_callback_data, self.config),
            CalendarScope.MONTHS:
                CalendarMonthView(self._item_callback_data, self.config),
            CalendarScope.YEARS:
                CalendarYearsView(self._item_callback_data, self.config),
        }

FORBIDDEN_DATE = Const("❌")

class ViewCalendarDays(CalendarDaysView):
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
        if selected_date == today:
            text = self.today_text
        elif selected_date in  data.get("forbidden", []):
            text = FORBIDDEN_DATE
        else:
            text = self.date_text
        raw_date = int(mktime(selected_date.timetuple()))
        return InlineKeyboardButton(
            text=await text.render_text(
                current_data, manager,
            ),
            callback_data=self.callback_generator(str(raw_date)),
        )
