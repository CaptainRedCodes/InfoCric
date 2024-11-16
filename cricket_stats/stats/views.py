from venv import logger
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .services import CricketAPIService

class PlayerSearchView(View):
    template_name = 'stats/search.html'
    cricket_service = CricketAPIService()

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        context = {}
        cricketer_name = request.POST.get('cricketer_name')

        try:
            # Search for player
            player_info = self.cricket_service.search_player(cricketer_name)
            if not player_info:
                messages.error(request, f"No player found with name: {cricketer_name}")
                return render(request, self.template_name, context)

            # Get all player information
            player_id = player_info['id']
            context.update({
                'stats': player_info,
                'player_details': self.cricket_service.get_player_details(player_id),
                'player_career': self.cricket_service.get_player_career(player_id),
                'player_stats': self.cricket_service.get_player_stats(player_id)
            })

        except:
            messages.error(request)
            logger.error(f"Error processing request: ")

        return render(request, self.template_name, context)