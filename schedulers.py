import streamlit as st
import logging
from datetime import time
import tableauserverclient as TSC

def main():
    st.title("Tableau Server Schedule Creator")

    # Input fields for server and authentication
    server_address = st.text_input("Server Address", "")
    site_name = st.text_input("Site Name", "")
    token_name = st.text_input("Personal Access Token Name", "")
    token_value = st.text_input("Personal Access Token Value", "", type="password")

    # Logging level selection
    logging_level = st.selectbox("Logging Level", ["debug", "info", "error"], index=2)
    logging.basicConfig(level=getattr(logging, logging_level.upper()))

    # Connect to Tableau Server
    if st.button("Connect to Server"):
        try:
            tableau_auth = TSC.PersonalAccessTokenAuth(token_name, token_value, site_id=site_name)
            server = TSC.Server(server_address, use_server_version=False)
            server.add_http_options({"verify": False})
            server.use_server_version()
            with server.auth.sign_in(tableau_auth):
                st.success("Connected to Tableau Server!")
        except Exception as e:
            st.error(f"Error connecting to Tableau Server: {e}")
            return

        # Schedule creation options
        st.header("Create Schedules")

        # Hourly schedule creation
        if st.checkbox("Create Hourly Schedule"):
            start_hourly = st.time_input("Start Time for Hourly Schedule", time(2, 30))
            end_hourly = st.time_input("End Time for Hourly Schedule", time(23, 0))
            interval_hourly = st.number_input("Interval (hours)", min_value=1, max_value=24, value=2)

            if st.button("Create Hourly Schedule"):
                hourly_interval = TSC.HourlyInterval(
                    start_time=start_hourly, end_time=end_hourly, interval_value=interval_hourly
                )
                hourly_schedule = TSC.ScheduleItem(
                    "Hourly-Schedule",
                    50,
                    TSC.ScheduleItem.Type.Extract,
                    TSC.ScheduleItem.ExecutionOrder.Parallel,
                    hourly_interval,
                )
                try:
                    hourly_schedule = server.schedules.create(hourly_schedule)
                    st.success(f"Hourly schedule created (ID: {hourly_schedule.id}).")
                except Exception as e:
                    st.error(f"Error creating hourly schedule: {e}")

        # Daily schedule creation
        if st.checkbox("Create Daily Schedule"):
            start_daily = st.time_input("Start Time for Daily Schedule", time(5, 0))

            if st.button("Create Daily Schedule"):
                daily_interval = TSC.DailyInterval(start_time=start_daily)
                daily_schedule = TSC.ScheduleItem(
                    "Daily-Schedule",
                    60,
                    TSC.ScheduleItem.Type.Subscription,
                    TSC.ScheduleItem.ExecutionOrder.Serial,
                    daily_interval,
                )
                try:
                    daily_schedule = server.schedules.create(daily_schedule)
                    st.success(f"Daily schedule created (ID: {daily_schedule.id}).")
                except Exception as e:
                    st.error(f"Error creating daily schedule: {e}")

        # Weekly schedule creation
        if st.checkbox("Create Weekly Schedule"):
            weekly_days = st.multiselect("Days for Weekly Schedule", [
                TSC.IntervalItem.Day.Monday,
                TSC.IntervalItem.Day.Tuesday,
                TSC.IntervalItem.Day.Wednesday,
                TSC.IntervalItem.Day.Thursday,
                TSC.IntervalItem.Day.Friday,
                TSC.IntervalItem.Day.Saturday,
                TSC.IntervalItem.Day.Sunday
            ], default=[TSC.IntervalItem.Day.Monday])

            start_weekly = st.time_input("Start Time for Weekly Schedule", time(19, 15))

            if st.button("Create Weekly Schedule"):
                weekly_interval = TSC.WeeklyInterval(start_time=start_weekly, *weekly_days)
                weekly_schedule = TSC.ScheduleItem(
                    "Weekly-Schedule",
                    70,
                    TSC.ScheduleItem.Type.Extract,
                    TSC.ScheduleItem.ExecutionOrder.Serial,
                    weekly_interval,
                )
                try:
                    weekly_schedule = server.schedules.create(weekly_schedule)
                    st.success(f"Weekly schedule created (ID: {weekly_schedule.id}).")
                except Exception as e:
                    st.error(f"Error creating weekly schedule: {e}")

        # Monthly schedule creation
        if st.checkbox("Create Monthly Schedule"):
            start_monthly = st.time_input("Start Time for Monthly Schedule", time(23, 30))
            day_of_month = st.number_input("Day of Month", min_value=1, max_value=31, value=15)

            if st.button("Create Monthly Schedule"):
                monthly_interval = TSC.MonthlyInterval(start_time=start_monthly, interval_value=day_of_month)
                monthly_schedule = TSC.ScheduleItem(
                    "Monthly-Schedule",
                    80,
                    TSC.ScheduleItem.Type.Subscription,
                    TSC.ScheduleItem.ExecutionOrder.Parallel,
                    monthly_interval,
                )
                try:
                    monthly_schedule = server.schedules.create(monthly_schedule)
                    st.success(f"Monthly schedule created (ID: {monthly_schedule.id}).")
                except Exception as e:
                    st.error(f"Error creating monthly schedule: {e}")

if __name__ == "__main__":
    main()
