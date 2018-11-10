from django.conf import settings
from django.templatetags.static import static
from discord import Webhook, RequestsWebhookAdapter, Embed


class WarehouseWebhook(Webhook):
    """Singleton class for SkyWare webhook."""

    def send_new_blueprint(self, bp, request):
        """Notify the creation of the new blueprint <bp> via webhook. <request> context is
        requiered, because we have to build absolute URIs."""

        if bp.author.avatar:
            avatar_url = bp.author.avatar.url
        else:
            avatar_url = static('warehouse/img/nouser.png')
        
        if bp.image:
            thumbnail_url = bp.image.url
        else:
            thumbnail_url = static('warehouse/img/nopic.png')
        
        embed = Embed(
            title = f"{bp.categ}: {bp}",
            description = 
            f"{bp.author} just added something new among the {bp.categ}. Check it out!",
            url = request.build_absolute_uri(bp.get_absolute_url())
        )
        embed.set_author(
            name = bp.author,
            url = request.build_absolute_uri(bp.author.get_absolute_url()),
            icon_url = request.build_absolute_uri(avatar_url)
        )
        embed.set_image(url=request.build_absolute_uri(thumbnail_url))
        embed.set_footer(text="Skywa.re - The Skywanderers Blueprints archive")
        self.send(embed=embed)


webhook = WarehouseWebhook.partial(
    settings.WEBHOOK_ID,
    settings.WEBHOOK_TOKEN,
    adapter=RequestsWebhookAdapter()
)