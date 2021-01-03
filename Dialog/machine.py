

class Dialog:

    def is_num_or_denom(self, group=None):
        return '1'

    def which_class_is_now(self, group=None):
        return '2'

    def which_class_is_next(self, group=None):
        return '3'

    def today_schedule(self, group=None):
        return '4'

    def when_class_begins_on(self, group=None, requested_date=None):
        return '5'

    def what_schedule_on(self, gropu=None, requested_date=None):
        return '6'

    def when_classes_ends_on(self, group, requested_date):
        return '7'

    def not_understood(self):
        return 'NU 8'

    def welcome(self):
        return '9'

    def error(self):
        return 'Err 10'

    def undefined(self):
        return 'Und 11'

    def ok_saved(self):
        return 'Ok'




    def handle_dialog(self, request=None, response=None):
        """
        :param request: user request
        :type request: str
        :param response: response to user
        """
        used_id = request['session']['user_id']
        # TODO: получить все переменные из запроса, если они есть:
        group = None    # Здесь получаем инфо о группе из базы
        state = None    # Здесь получаем инфо о состоянии из базы
        request_type = None     # Здесь мы получаем тип запроса из request
        requested_date = None   # Здесь мы получаем дату, если запрос с датой
        requested_faculty = None    # Здесь мы храним факультет, если запрос с факультетом
        requested_department = None  # Здесь мы храним группу, если запрос с группой
        requested_group_num = None  # Здесь мы храним номер группы, если таков запрсо

        response_text = 'None'
        if state == 'base':
            if request_type == 'is_num_or_denum':
                response_text = self.is_num_or_denom(group)
            elif request_type == 'which_class_is_now':
                response_text = self.which_class_is_now(group)
            elif request_type == 'which_class_is_next':
                response_text = self.which_class_is_next(group)
            elif request_type == 'today_schedule':
                response_text = self.today_schedule(group)
            elif request_type == 'when_classes_begins_on':
                response_text = self.when_class_begins_on(group, requested_date)
            elif request_type == 'when_classes_begins_on':
                response_text = self.when_class_begins_on(group, requested_date)
            elif request_type == 'what_schedule_on':
                response_text = self.what_schedule_on(group, requested_date)
            elif request_type == 'when_classes_ends_on':
                response_text = self.when_classes_ends_on(group, requested_date)
            elif request_type == 'not_understood':
                response_text = self.not_understood()
            elif request_type == 'change_group':
                # TODO: запись состояния в базу
                state = 'welcome'
                response_text = self.welcome()
            else:
                response_text = self.error()

        elif state == 'welcome':
            # TODO: Что алиса делает в состоянии 'Welcome'?
            response_text = self.undefined()
            # TODO: запись состояния в базу
            state = 'select_faculty'

        elif state == 'select_faculty':
            if request_type == 'valid_faculty':
                # TODO: запись факультета в базу
                faculty = requested_faculty
                # TODO: запись состояния в базу
                state = 'select_department'
                response_text = self.ok_saved()
            elif request_type == 'not_understood':
                response_text = self.not_understood()
            else:
                response_text = self.error()

        elif state == 'select_department':
            if request_type == 'valid_department':
                # TODO: запись кафедры в базу
                department = requested_department
                # TODO: запись состояния в базу
                state = 'select_group_number'
                response_text = self.ok_saved()
            elif request_type == 'not_understood':
                response_text = self.not_understood()
            else:
                response_text = self.error()

        elif state == 'select_group_number':
            if request_type == 'valid_group_number':
                # TODO: запись номера группы в базу
                department = requested_group_num
                # TODO: запись состояния в базу
                state = 'base'
                response_text = self.ok_saved()
            elif request_type == 'not_understood':
                response_text = self.not_understood()
            else:
                response_text = self.error()
