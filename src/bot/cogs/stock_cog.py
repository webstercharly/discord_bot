from discord.ext import commands
from bot.config_loader import config_loader
from discord.ui import View, Button
from discord import Interaction, utils, ButtonStyle, Embed, Color, ui
import aiohttp

class StockCog(commands.Cog):
    def __init__(self, bot):
        self.cog_name = "stock_cog"
        self.bot = bot
        self.config = {}
        self.base_url = 'https://dev.sellix.io/v1/products'

    async def setup(self):
        self.config = await config_loader.load_config(self.cog_name)
        config_loader.subscribe(self.on_config_update)

    async def on_config_update(self, config_name: str):
        if config_name == self.cog_name:
            print(f"{self.__class__.__name__} received update for {config_name}")
            self.config = await config_loader.load_config(self.cog_name)
            print("RulesCog configuration reloaded:", self.config)

    @commands.command()
    async def stock(self, ctx):
        try:
            await ctx.message.delete()
            if not self.config["cog_enabled"]:
                await ctx.send("This cog is disabled.", delete_after=30)
                return

            owner_role = utils.get(ctx.guild.roles, name="Owner")

            if ctx.channel.id != self.config["stock_channel_id"] and (owner_role not in ctx.author.roles):
              await ctx.send("This command can only be used in the stock channel.", delete_after=20)
              return


            request_headers = {'Authorization': f'Bearer {self.config["sellix_api_key"]}'}

            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, headers=request_headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        sorted_products = sorted(
                            [product for product in data['data']["products"]
                            if not (product["private"] or product["on_hold"] or product["unlisted"] or product["stock"] == 0)],
                            key=lambda x: x['price']
                        )
                        if len(sorted_products) == 0:
                            await ctx.send("Unfortunately, we are currently out of stock", delete_after=30)
                            return

                        for product in sorted_products:
                          embed = Embed(title="🛒 Product Stock (Sellix)", description="All available products and their stock, sorted by price.", color=int("1F8B4C",16))
                          cloudflare_image_url = f"https://imagedelivery.net/95QNzrEeP7RU5l5WdbyrKw/{product['cloudflare_image_id']}/shopitem" # This URL may be different for your store
                          embed.set_thumbnail(url=self.config["embed"]["image_thumbnail_url"])
                          embed.set_image(url=cloudflare_image_url)
                          product_url = self.config["sellix_product_url"] + product['slug']

                          if product['price_discount'] > 0:
                              original_price = product['price']
                              discount_amount = original_price * (product['price_discount'] / 100)
                              discounted_price = original_price - discount_amount
                              price_field_value = f"~~${original_price}~~ ${round(discounted_price,2)} (-{product['price_discount']}%)"
                          else:
                              discounted_price = product['price']
                              price_field_value = f"${discounted_price}"

                          embed.add_field(name="Stock", value=str(product['stock']), inline=True)
                          embed.add_field(name="Price", value=price_field_value, inline=True)
                          embed.add_field(name="Product URL", value=f"[View Product]({product_url})", inline=True)
                          embed.set_footer(text="Need help? Contact Support")
                          await ctx.send(embed=embed, delete_after=30)
                    else:
                        await ctx.send("Failed to retrieve product stock information.", delete_after=30)
        except Exception as e:
            print(e)


async def setup(bot):
    cog = StockCog(bot)
    await cog.setup()
    await bot.add_cog(cog)
