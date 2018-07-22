defmodule MALWeb.PageController do
  use MALWeb, :controller

  def index(conn, _params) do
    render conn, "index.html"
  end
end
