import argparse
import logging
from datetime import time
import tableauserverclient as TSC

def create_hourly_schedule(server):
    # Hourly Schedule
    hourly_interval = TSC.HourlyInterval(start_time=time(2, 30), end_time=time(23, 0), interval_value=2)
    hourly_schedule = TSC.ScheduleItem(
        "Hourly-Schedule",
        50,
        TSC.ScheduleItem.Type.Extract,
        TSC.ScheduleItem.ExecutionOrder.Parallel,
        hourly_interval,
    )
    try:
        hourly_schedule = server.schedules.create(hourly_schedule)
        print(f"Hourly schedule created (ID: {hourly_schedule.id}).")
    except Exception as e:
        print(f"Error creating hourly schedule: {e}")


def create_daily_schedule(server):
    # Daily Schedule
    daily_interval = TSC.DailyInterval(start_time=time(5))
    daily_schedule = TSC.ScheduleItem(
        "Daily-Schedule",
        60,
        TSC.ScheduleItem.Type.Subscription,
        TSC.ScheduleItem.ExecutionOrder.Serial,
        daily_interval,
    )
    try:
        daily_schedule = server.schedules.create(daily_schedule)
        print(f"Daily schedule created (ID: {daily_schedule.id}).")
    except Exception as e:
        print(f"Error creating daily schedule: {e}")


def create_weekly_schedule(server):
    # Weekly Schedule
    weekly_interval = TSC.WeeklyInterval(
        time(19, 15), TSC.IntervalItem.Day.Monday, TSC.IntervalItem.Day.Wednesday, TSC.IntervalItem.Day.Friday
    )
    weekly_schedule = TSC.ScheduleItem(
        "Weekly-Schedule",
        70,
        TSC.ScheduleItem.Type.Extract,
        TSC.ScheduleItem.ExecutionOrder.Serial,
        weekly_interval,
    )
    try:
        weekly_schedule = server.schedules.create(weekly_schedule)
        print(f"Weekly schedule created (ID: {weekly_schedule.id}).")
    except Exception as e:
        print(f"Error creating weekly schedule: {e}")


def create_monthly_schedule(server):
    # Monthly Schedule
    monthly_interval = TSC.MonthlyInterval(start_time=time(23, 30), interval_value=15)
    monthly_schedule = TSC.ScheduleItem(
        "Monthly-Schedule",
        80,
        TSC.ScheduleItem.Type.Subscription,
        TSC.ScheduleItem.ExecutionOrder.Parallel,
        monthly_interval,
    )
    try:
        monthly_schedule = server.schedules.create(monthly_schedule)
        print(f"Monthly schedule created (ID: {monthly_schedule.id}).")
    except Exception as e:
        print(f"Error creating monthly schedule: {e}")


def main():
    parser = argparse.ArgumentParser(description="Creates sample schedules for each type of frequency.")
    # Common options
    parser.add_argument("--server", "-s", required=True, help="server address")
    parser.add_argument("--site", "-S", help="site name")
    parser.add_argument("--token-name", "-p", required=True, help="name of the personal access token used to sign into the server")
    parser.add_argument("--token-value", "-v", required=True, help="value of the personal access token used to sign into the server")
    parser.add_argument(
        "--logging-level",
        "-l",
        choices=["debug", "info", "error"],
        default="error",
        help="desired logging level (set to error by default)",
    )

    args = parser.parse_args()

    # Set logging level
    logging_level = getattr(logging, args.logging_level.upper())
    logging.basicConfig(level=logging_level)

    tableau_auth = TSC.PersonalAccessTokenAuth(args.token_name, args.token_value, site_id=args.site)
    server = TSC.Server(args.server, use_server_version=False)
    server.add_http_options({"verify": False})
    server.use_server_version()

    with server.auth.sign_in(tableau_auth):
        print("\nScheduler Creation Menu")
        print("1. Create Hourly Schedule")
        print("2. Create Daily Schedule")
        print("3. Create Weekly Schedule")
        print("4. Create Monthly Schedule")
        print("5. Create All Schedules")
        print("6. Exit")

        while True:
            choice = input("\nEnter your choice (1-6): ")
            if choice == "1":
                create_hourly_schedule(server)
            elif choice == "2":
                create_daily_schedule(server)
            elif choice == "3":
                create_weekly_schedule(server)
            elif choice == "4":
                create_monthly_schedule(server)
            elif choice == "5":
                create_hourly_schedule(server)
                create_daily_schedule(server)
                create_weekly_schedule(server)
                create_monthly_schedule(server)
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
