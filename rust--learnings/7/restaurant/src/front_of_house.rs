pub mod hosting;

mod front_of_house {
    mod serving {
        fn take_order() {}

        fn serve_order() {}

        fn take_payment() {}
    }

    fn fix_incorrect_order() {
        cook_order();
    }

    fn cook_order() {}
}
