# This file is responsible for configuring your application
# and its dependencies with the aid of the Mix.Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.
use Mix.Config

# General application configuration
config :mal,
  namespace: MAL,
  ecto_repos: [MAL.Repo]

# Configures the endpoint
config :mal, MALWeb.Endpoint,
  url: [host: "localhost"],
  secret_key_base: "v0qW975nptH39cnf8iwBUa7q41VqD1tHPRGkGVscRitYKKqS3lx5yMdz/CS14XT+",
  render_errors: [view: MALWeb.ErrorView, accepts: ~w(html json)],
  pubsub: [name: MAL.PubSub,
           adapter: Phoenix.PubSub.PG2]

# Configures Elixir's Logger
config :logger, :console,
  format: "$time $metadata[$level] $message\n",
  metadata: [:user_id]

# Import environment specific config. This must remain at the bottom
# of this file so it overrides the configuration defined above.
import_config "#{Mix.env}.exs"
