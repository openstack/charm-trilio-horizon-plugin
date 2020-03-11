from django import template
from openstack_dashboard import api
from openstack_dashboard import policy
from datetime import datetime
from django.template.defaultfilters import stringfilter
import pytz

register = template.Library()


@register.filter(name="getusername")
def get_user_name(user_id, request):
    user_name = user_id
    if policy.check((("identity", "identity:get_user"),), request):
        try:
            user = api.keystone.user_get(request, user_id)
            if user:
                user_name = user.username
        except Exception:
            pass
    return user_name


@register.filter(name="getprojectname")
def get_project_name(project_id, request):
    project_name = project_id
    try:
        project_info = api.keystone.tenant_get(request, project_id, admin=True)
        if project_info:
            project_name = project_info.name
    except Exception:
        pass
    return project_name


def get_time_zone(request):
    tz = "UTC"
    try:
        tz = request._get_cookies()["django_timezone"]
    except Exception:
        try:
            tz = request.COOKIES["django_timezone"]
        except Exception:
            pass

    return tz


def get_local_time(record_time, input_format, output_format, tz):
    """
    Convert and return the date and time - from GMT to local time
    """
    try:
        if not record_time or record_time is None or record_time == "":
            return ""
        else:
            if not input_format or input_format is None or input_format == "":
                input_format = "%Y-%m-%dT%H:%M:%S.%f"
            if (
                not output_format or
                output_format is None or
                output_format == ""
            ):
                output_format = "%m/%d/%Y %I:%M:%S %p"

            local_time = datetime.strptime(record_time, input_format)
            local_tz = pytz.timezone(tz)
            from_zone = pytz.timezone("UTC")
            local_time = local_time.replace(tzinfo=from_zone)
            local_time = local_time.astimezone(local_tz)
            local_time = datetime.strftime(local_time, output_format)
            return local_time
    except Exception:
        pass
        return record_time


@register.filter(name="gettime")
def get_time_for_audit(time_stamp, request):
    display_time = time_stamp
    try:
        time_zone_of_ui = get_time_zone(request)
        display_time = get_local_time(
            time_stamp,
            "%I:%M:%S.%f %p - %m/%d/%Y",
            "%I:%M:%S %p - %m/%d/%Y",
            time_zone_of_ui,
        )
    except Exception:
        pass
    return display_time


@register.filter(name="getsnapshotquantifier")
def display_time_quantifier(seconds):
    intervals = (
        ("weeks", 604800),  # 60 * 60 * 24 * 7
        ("days", 86400),  # 60 * 60 * 24
        ("hours", 3600),  # 60 * 60
        ("minutes", 60),
        ("seconds", 1),
    )

    result = []
    granularity = 4
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip("s")
            result.append("{} {}".format(value, name))
        else:
            # Add a blank if we're in the middle of other values
            if len(result) > 0:
                result.append(None)
    return ", ".join([x for x in result[:granularity] if x is not None])


@register.filter(name="custom_split")
@stringfilter
def custom_split(value, key):
    key = int(key)
    return value.split("_")[key]
