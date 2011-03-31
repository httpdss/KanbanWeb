from datetime import datetime, date, timedelta
from django.shortcuts import render_to_response, get_object_or_404
from kanban.sprints.models import Sprints
from kanban.tickets.models import Tickets
from django.db.models import Q

def index(req):
    sprints = Sprints.objects.order_by('date_to')
    return render_to_response('sprints/index.html', { 'sprints' : sprints, })
#enddef

def detail(req, sprint_id):
    sprint = Sprints.objects.get(pk=sprint_id)
    if sprint.date_to > datetime.now():
        tickets = Tickets.objects.filter( Q(done_date__isnull=True) | Q(done_date__lte=sprint.date_to, done_date__gt=sprint.date_from))
        dates = []
        todo = []
        devel = []
        done = []
        #for i in xrange(sprint.date_from.toordinal(), sprint.date_to.toordinal()+1):
        df = sprint.date_from
        addday = timedelta(days=1)
        while df <= sprint.date_to:
            todo_value = 0
            devel_value = 0
            done_value = 0
            if df.date() == date.today():
                break;
            else:
                if df.isoweekday() not in (6, 7):
                    dates.append(df)
                    for item in tickets:
                        if item.done_date is not None and item.done_date <= df:
                            done_value = done_value+1
                        #endif
                        if item.devel_date is not None and item.devel_date <= df:
                            devel_value = devel_value+1
                        #endif
                        if item.pub_date <= df and item.done_date is None and item.devel_date is None:
                            todo_value = todo_value+1
                        #endif
                    #endfor
                    done.append(done_value)
                    devel.append(done_value+devel_value)
                    todo.append(done_value+devel_value+todo_value)
                else:
                    pass
                #endif
            #endif
            df = df+addday
        #endwhile
    #endif
    return render_to_response('sprints/detail.html', {
        'sprint' : sprint,
        'tickets' : tickets,
        'dates' : dates,
        'done' : done,
        'devel' : devel,
        'todo' : todo,
    })
#enddef
